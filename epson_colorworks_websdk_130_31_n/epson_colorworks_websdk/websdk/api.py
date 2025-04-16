#
# Epson Label Printer Web SDK
#
# Created by Seiko Epson Corporation on 2021/9/8.
# Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
#

from flask import Blueprint, current_app
from flask import request
from flask_restful import Api, Resource
import json
import re
import base64
import mimetypes
import math
import os
from chardet import detect
from error import *
from functools import reduce
from typing import Optional

import subprocess
from flask import jsonify

import tempfile
from enum import IntEnum


class Status_group(IntEnum):
    BeforeComm = 0
    FatalError = 1
    Error = 2
    Pause = 3
    Printing = 4
    Warning = 5
    Others = 6


class Context:
    '''
    Context caches several information which may take time to fetch.
    Its life time is from the beginning to the end of request.
    '''

    def __init__(self):
        self.queue_list = None
        self.printer_info = None


api_bp = Blueprint('api', __name__)

BASE_PATH = '/api/v1/printers'
ELPU_PATH = '/opt/epson/epson-label-printer-utility/elpu'
ELPU_TIMEOUT_SEC = 10


def num_typeof_str(n: str) -> Optional[type]:
    try:
        float(n)
    except ValueError:
        return None
    else:
        if float(n).is_integer():
            return int
        else:
            return float


def run_printer_utl(args: list) -> subprocess.CompletedProcess:
    '''Suppresses TimeoutExpired exception for subprocess.run()'''
    try:
        cmd = [ELPU_PATH] + args
        current_app.logger.debug(cmd)
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=ELPU_TIMEOUT_SEC)
    except subprocess.TimeoutExpired as e:
        raise PrinterNotConnectedError() from e


def get_print_capability(context: Context, queue_name: str) -> dict:
    model_id = get_model_id(context, queue_name)
    jsonpath = '/resources/{}/print_capability.json'.format(model_id)

    with open(os.path.dirname(__file__) + jsonpath, 'r') as f:
        return json.load(f)


def get_printer_capability(context: Context, queue_name: str) -> list:
    model_id = get_model_id(context, queue_name)
    jsonpath = '/resources/{}/printer_capability.json'.format(model_id)

    with open(os.path.dirname(__file__) + jsonpath, 'r') as f:
        return json.load(f)


def get_command_conversions(context: Context, queue_name: str) -> dict:
    model_id = get_model_id(context, queue_name)
    jsonpath = '/resources/{}/command_conversion.json'.format(model_id)

    with open(os.path.dirname(__file__) + jsonpath, 'r') as f:
        return json.load(f)


def append_sidemargin_option_implicitly(optionlist: list):
    opt_paperform = next(
        filter(lambda x: x.startswith('paperForm='), optionlist), None)

    if opt_paperform:
        paperform = opt_paperform.lstrip('paperForm=')
        if paperform in {'DL', 'CL'}:
            optionlist.append('sideMargin=47')
        elif paperform in {'CP', 'WB'}:
            optionlist.append('sideMargin=0')


# Only px(600dpi) to mm
def dot_to_len(dot: int) -> float:
    return math.floor(float(abs(dot)) / 600.0 * 25.4 * 10.0 + 0.5) / 10.0 * (-1 if dot < 0 else 1)

# Only mm to px(600dpi)


def len_to_dot(len: float) -> int:
    return int(float(abs(len)) / 25.4 * 600 + 0.5) * (-1 if len < 0 else 1)


def get_queue_list(context: Context) -> list:
    try:
        if context and context.queue_list:
            return context.queue_list

        data = []
        arg = ['-l']
        # cp = subprocess.run(['lpstat', '-a'], stdout = subprocess.PIPE)
        cp = run_printer_utl(arg)

        cp_str = cp.stdout.decode('utf-8')
        lines = cp_str.split(sep='\n')

        for line in lines:
            items = line.split()
            if items:
                data.append(items[1])

        context.queue_list = data
        return (data)

    except Exception as e:
        raise e


def is_valid_queue(context: Context, queue_name: str) -> bool:
    try:
        queue_list = get_queue_list(context)
        if queue_name in queue_list:
            return True
        else:
            return False

    except Exception as e:
        raise e


def get_printer_info(context: Context, queue_name: str) -> dict:
    if not is_valid_queue(context, queue_name):
        raise InvalidQueueNameError(queue_name)

    if context and context.printer_info:
        return context.printer_info

    data = {}

    # info
    optionlist = ['deviceID', 'inkNameK', 'inkNameC',
                  'inkNameM', 'inkNameY', 'inkNameMN']
    arg = sum(map(lambda x: ['-o', x], optionlist), [])
    # -n DryMode
    # param = ['-p', queue_name, '-n']
    param = ['-p', queue_name]

    cp = run_printer_utl(param + arg)
    cp_str = cp.stdout.decode('utf-8')

    lines = cp_str.split(sep='\n')
    for line in lines:
        items = line.split(':', 1)
        if not items:
            pass
        else:
            if len(items) != 1:
                data[items[0].strip()] = items[1].strip()
            elif len(items[0]) != 1:
                pass
    # DEBUG
    # print(data)

    context.printer_info = data
    return data


def get_model_name(context: Context, queue_name: str) -> str:
    device_id = get_printer_info(context, queue_name)['deviceID']

    for field in device_id.split(';'):
        if field.startswith('MDL:'):
            model_id = field.replace('MDL:', '')
            return model_id

    raise InternalServerError()


def get_model_id(context: Context, queue_name: str) -> str:
    model_name = get_model_name(context, queue_name)

    with open(os.path.dirname(__file__) + '/resources/modelid_map.json', 'r') as f:
        dict = json.load(f)

        for k, v in dict.items():
            if model_name in v:
                return k

    raise InternalServerError()

def is_pagesize_model_id(context: Context, queue_name: str) -> bool:
    model_id = get_model_id(context, queue_name)
    PAGESIZE_PRINTER = ['CW-C6000A_C6500A_Series','CW-C6000P_C6500P_Series']

    if model_id in PAGESIZE_PRINTER:
        return True
    else:
        return False

    raise InternalServerError()

def get_printer_status(context: Context, queue_name: str) -> dict:
    try:
        if not is_valid_queue(context, queue_name):
            raise InvalidQueueNameError(queue_name)

        data = {}
        # status
        optionlist = ['status', 'statusGroup']
        arg = sum(map(lambda x: ['-o', x], optionlist), [])
        # DEBUG  -n DryMode
        # param = ['-p', queue_name, '-n']
        param = ['-p', queue_name]

        cp = run_printer_utl(param + arg)
        cp_str = cp.stdout.decode('utf-8')

        lines = cp_str.split(sep='\n')
        for line in lines:
            items = line.split(':', 1)
            if not items:
                pass
            else:
                if len(items) != 1:
                    item_list = items[1].split(',')
                    if len(item_list) != 1:
                        data[items[0].strip()] = int(item_list[0].strip())
                        if items[0].strip() == 'status':
                            data['statusDescription'] = item_list[1].strip()
                        elif items[0].strip() == 'statusGroup':
                            data['statusGroupDescription'] = item_list[1].strip()
                    else:
                        data[items[0].strip()] = items[1].strip()
                elif len(items[0]) != 1:
                    pass
        # DEBUG
        # print(data)

        current_app.logger.debug(data)
        return data

    except Exception as e:
        raise e


def get_printer_status_group(context: Context, queue_name: str) -> int:
    try:
        if not is_valid_queue(context, queue_name):
            raise InvalidQueueNameError(queue_name)

        data = get_printer_status(context, queue_name)
        return data['statusGroup']

    except Exception as e:
        raise e


def make_custom_object_from_lpoptions(context: Context, queue_name: str) -> Optional[dict]:
    try:

        if not is_valid_queue(context, queue_name):
            raise InvalidQueueNameError(queue_name)

        w = ''  # width
        h = ''  # Height
        lpoptions_path = os.environ['HOME'] + "/.cups/lpoptions"
        # print(lpoptions_path)
        if os.path.exists(lpoptions_path):
            with open(lpoptions_path, 'rb') as f:  # open file as binary
                b = f.read()  # read file
                # DEBUG
                # print(b)  # b'\x82\xb1\x82\xcc\x83t\x83@\x83C……\xa2\x82\xdc\x82\xb7\r\n'
                enc = detect(b)  # check encoding by chardet.detect()
                with open(lpoptions_path, encoding=enc['encoding']) as f:
                    s = f.read()
                    # DEBUG
                    # print(repr(s))
                    lines = s.split('\n')
                    for line in lines:
                        items = line.split(' ')
                        if queue_name in items:
                            for item in items:
                                # Since the key 'PageSize' is only supported by CW-C6000A_C6500A_Series,CW-C6000P_C6500P_Series,
                                # Other models have to be replaced with 'media' instead.
                                if not is_pagesize_model_id(context, queue_name):
                                    if 'media' in item:
                                        values = item.split('=')
                                        if len(values) != 1:
                                            if 'Custom' in item:
                                                v = item.split('=')
                                                # TODO str.translate()
                                                r = v[1].replace('\n', '')
                                                r = r.replace('mm', '')
                                                r = r.replace('Custom.', '')
                                                w = r.split('x')[0]
                                                h = r.split('x')[1]
                                else:
                                    if 'PageSize' in item:
                                        values = item.split('=')
                                        if len(values) != 1:
                                            if 'Custom' in item:
                                                v = item.split('=')
                                                # TODO str.translate()
                                                r = v[1].replace('\n', '')
                                                r = r.replace('mm', '')
                                                r = r.replace('Custom.', '')
                                                w = r.split('x')[0]
                                                h = r.split('x')[1]

        else:
            pass

        if num_typeof_str(w) and num_typeof_str(h):
            return {'CustomWidth': float(w), 'CustomHeight': float(h)}
        else:
            return None

    except Exception as e:
        raise e


def make_capability_from_lpoptions(context: Context, queue_name: str) -> list:
    try:
        if not is_valid_queue(context, queue_name):
            raise InvalidQueueNameError(queue_name)

        cmd = ['lpoptions', '-p', queue_name, '-l']
        current_app.logger.debug(cmd)
        cp = subprocess.run(cmd, stdout=subprocess.PIPE)
        cp_str = cp.stdout.decode('utf-8')

        if not cp_str:
            raise InvalidQueueNameError(queue_name)

        lines = cp_str.split(sep='\n')

        additionaldict = get_print_capability(context, queue_name)

        # Respose Data
        datalist = []
        for line in lines:
            if line:
                datadic = {}
                cap_values = []
                datadic['values'] = cap_values
                key_value = line.split(':')

                # Key
                key = key_value[0]
                key = key.split('/')
                cap_name = key[0]

                # Mandatory Response value
                datadic['name'] = cap_name
                datadic['type'] = 'string'  # string/num
                datadic['capabilitytype'] = 'array'  # array/boolean/range

                # Value
                values = key_value[1]
                values = values.split()

                if additionaldict.get(cap_name):
                    datadic.update(additionaldict[cap_name])

                # DEBUG
                # print(values)
                for value in values:
                    # Judge capabilitytype form current value
                    if value.startswith('*'):
                        currentvalue = value[1:]
                        datadic['current'] = currentvalue
                        cap_values.append(currentvalue)

                        # numeric
                        if num_typeof_str(currentvalue):
                            datadic['type'] = 'num'
                            datadic['capabilitytype'] = 'range'

                            if num_typeof_str(currentvalue) is int:
                                datadic['current'] = int(currentvalue)
                            else:
                                datadic['current'] = float(currentvalue)

                        # TODO only 'True/False'?
                        if currentvalue in ['True', 'False']:
                            datadic['capabilitytype'] = 'boolean'
                            datadic['type'] = 'boolean'
                            if currentvalue == 'True':
                                datadic['current'] = True
                            else:
                                datadic['current'] = False

                        # pagesize media
                        if 'pagesize' == cap_name.casefold():
                            datadic['type'] = 'pagesize'
                            # Custom.WIDTHxHEIGHT
                            if 'custom' in currentvalue.casefold():
                                customsize = make_custom_object_from_lpoptions(
                                    context,
                                    queue_name)

                                if customsize:
                                    datadic['current'] = customsize
                                else:  
                                    # Did not find the information of custom size values in this process environment.
                                    # Since we are not able to access to the custom size values which have been set with lpadmin,
                                    # we fallback to the other available standard size.
                                    currentvalue = next(
                                        filter(lambda x: not x.startswith('*'), values), None)

                                    # Since the key 'PageSize' is only supported by CW-C6000A_C6500A_Series,CW-C6000P_C6500P_Series,
                                    # Other models have to be replaced with 'media' instead.
                                    current_app.logger.debug('make_capability_from_lpoptions')
                                    if not is_pagesize_model_id(context, queue_name):
                                        cmd = ['lpoptions', '-p', queue_name,
                                            '-o', 'media={}'.format(currentvalue)]
                                    else:
                                        cmd = ['lpoptions', '-p', queue_name,
                                        '-o', 'PageSize={}'.format(currentvalue)]

                                    current_app.logger.debug(cmd)
                                    subprocess.run(cmd, stdout=subprocess.PIPE)

                                    datadic['current'] = currentvalue

                    # Not current value
                    else:
                        cap_values.append(value)

                if datadic['type'] == 'num':
                    valuesmap = map(
                        (lambda x: int(x[1:]) if x.startswith('*') else int(x)), values)
                    valueslist = list(map(int, valuesmap))
                    # DEBUG
                    # print('MAX VALUE : ',maxv,'MIN_VALUE : ',minv,'STEP : ',step)
                    datadic['max'] = max(valueslist)
                    datadic['min'] = min(valueslist)

                    if len(valueslist) >= 2:
                        datadic['step'] = abs(valueslist[-1] - valueslist[-2])
                    else:
                        datadic['step'] = 0

                    del datadic['values']

                if datadic['type'] == 'boolean':
                    del datadic['values']
                datalist.append(datadic)
        # DEBUG
        # print(datalist)
        # return jsonify(datalist)
        return datalist

    except Exception as e:
        raise e


def make_capability_from_elpu(context: Context, queue_name: str, with_currentvalue: bool = True) -> list:
    try:
        if not is_valid_queue(context, queue_name):
            raise InvalidQueueNameError(queue_name)

        capability = get_printer_capability(context, queue_name)

        if not with_currentvalue:
            return capability

        command_conversions = get_command_conversions(context, queue_name)

        # Get option keys from json
        # optionlist = ['PaperSource', 'paperShape', 'paperForm', 'formDetectionType', 'formGap', 'printQuality', 'cutPosition', 'printPositionV', 'printPositionH']
        optionlist = []
        for v in capability:
            opt_comb = command_conversions['option_combinations'].get(
                v['name'])
            if opt_comb:
                optionlist.extend(opt_comb)
            else:
                optionlist.append(v['name'])

        arg = sum(map(lambda x: ['-o', x], optionlist), [])
        # -n DryMode Debug mode
        # param = ['-p', queue_name, '-n']
        param = ['-p', queue_name]

        # Get current setting values
        cp = run_printer_utl(param + arg)
        cp_str = cp.stdout.decode('utf-8')

        data = {}
        lines = cp_str.split(sep='\n')
        for line in lines:
            items = line.split(':')
            if items:
                if len(items) != 1:
                    data[items[0]] = items[1]

                else:
                    data[items[0]] = ''
        del data['']

        # DEBUG
        # print(data)

        def current_for_combination(opt_comb: list, cmd_comb: dict, data: dict) -> Optional[str]:
            val = {i: data[i].strip() for i in opt_comb}

            for k, v in cmd_comb.items():
                if v == val:
                    return k

            return None

        # Set current setting values
        for v in capability:
            opt_comb = command_conversions['option_combinations'].get(
                v['name'])
            if opt_comb and set(opt_comb).issubset(data.keys()):
                cmd_comb = command_conversions['command_combinations'].get(
                    v['name'])
                if cmd_comb:
                    v['current'] = current_for_combination(
                        opt_comb, cmd_comb, data)

            elif v['name'] in data:
                # dot to mm
                if v['name'] in ['formGap', 'cutPosition', 'printPositionH', 'printPositionV', 'sideMargin', 'rightMargin', 'edgeHole', 'peelPositionA', 'peelPositionB']:
                    if data[v['name']].strip():
                        if 'N/A' in data[v['name']]:
                            v['current'] = data[v['name']].strip()
                        else:
                            v['current'] = dot_to_len(
                                int(data[v['name']].strip()))
                else:
                    v['current'] = data[v['name']].strip()
        # DEBUG
        # print(capability)
        return capability

    except Exception as e:
        raise e


def is_inrange(value, min, max, step) -> bool:
    step_strlist = str(step).split('.')
    decimal_digit = len(step_strlist[1].rstrip(
        '0')) if len(step_strlist) > 1 else 0

    # To avoid rounding error, we shift all arguments to integer
    shift = 10 ** decimal_digit

    # If the value has decimal digit even it was shifted, we regard as False
    if not value == 0 and not float(value * shift).is_integer():
        return False

    value, min, max, step = map(lambda x: int(
        x * shift), (value, min, max, step))

    return value in range(min, max + 1, step)


def validate_setting(setting: dict, capability: list) -> dict:
    validated_setting = {}

    def conforms_to_type(value, cap: dict) -> bool:
        if cap['type'] == 'string' and type(value) is str:
            return True
        elif cap['type'] == 'num' and type(value) in (int, float):
            return True
        elif cap['type'] == 'boolean' and type(value) is bool:
            return True
        elif cap['type'] == 'pagesize' and type(value) in (str, dict):
            return True

        return False

    def specialized_rangecap_for_key(cap: dict, key: str) -> dict:
        new_cap = cap.copy()

        min, max = cap['min'], cap['max']

        # If min or max depends on key, check for it
        if type(min) is dict:
            new_cap['min'] = min[key]

        if type(max) is dict:
            new_cap['max'] = max[key]

        return new_cap

    def is_customsize_inrange(value, cap: dict) -> bool:
        widthCap = cap['customwidth']
        heightCap = cap['customheight']

        # Get the target media form
        form = setting.get('MediaForm')
        if not form:
            # Get the current media form
            form = next(filter(lambda x: x['name'] == 'MediaForm', capability), {}).get(
                'current')

        if form:
            # Get form specialized capability
            widthCap = specialized_rangecap_for_key(widthCap, form)
            heightCap = specialized_rangecap_for_key(heightCap, form)

        params = [
            (value['CustomWidth'], widthCap),
            (value['CustomHeight'], heightCap)
        ]

        # Check if the size is between range
        def is_between_range(size, range: dict) -> bool:
            min, max = range['min'], range['max']
            return min <= size and size <= max

        # Regard as valid if both width and height are valid
        return reduce(lambda x, y: x and y, map(lambda arg: is_between_range(*arg), params))

    def is_affect_paperform_inrange(value, cap: dict) -> bool:
        # Get the target paper form
        form = setting.get('paperForm')
        if not form:
            # Get the current paper form
            form = next(filter(lambda x: x['name'] == 'paperForm', capability), {}).get(
                'current')

        if form:
            # Get form specialized capability
            cap = specialized_rangecap_for_key(cap, form)

        return is_inrange(value, cap['min'], cap['max'], cap['step'])

    def is_cutinterval_inrange(value, cap: dict) -> bool:
        # Support for CW-C6520P/CW-C6020P Series
        if cap['min'] == cap['max']:
            return True

        return is_inrange(value, cap['min'], cap['max'], cap['step'])

    def conforms_to_capability_type(value, cap: dict) -> bool:
        if cap['capabilitytype'] == 'array':
            if cap['type'] == 'pagesize':
                if type(value) is dict and value.get('CustomWidth') and value.get('CustomHeight'):
                    return is_customsize_inrange(value, cap)

                else:
                    if value in cap['values'] and not value == 'Custom.WIDTHxHEIGHT':
                        return True

            else:
                if value in cap['values']:
                    return True

        elif cap['capabilitytype'] == 'range':
            if cap['name'] == 'formGap' or cap['name'] == 'sideMargin' or cap['name'] == 'rightMargin':
                return is_affect_paperform_inrange(value, cap)

            if cap['name'] == 'CutInterval':
                return is_cutinterval_inrange(value, cap)

            return is_inrange(value, cap['min'], cap['max'], cap['step'])

        elif cap['capabilitytype'] == 'boolean':
            if type(value) is bool:
                return True

        return False

    for cap in capability:
        key = cap['name']

        value = setting.get(key)
        if value is None:
            continue

        valid = conforms_to_type(
            value, cap) and conforms_to_capability_type(value, cap)

        if valid:
            validated_setting[key] = value
        else:
            current_app.logger.warning(
                '{} is unavailable for {}.'.format(value, key))
            raise SetParamError(key, str(value))

    return validated_setting


class List(Resource):
    def get(self):
        try:
            context = Context()

            data = get_queue_list(context)

            current_app.logger.debug((request, data))
            return jsonify(data)

        except Exception as e:
            current_app.logger.exception(e)
            return exc_to_http_ret(e)


class PrintCapability(Resource):
    def get(self, queue_name: str):
        try:
            context = Context()

            if not is_valid_queue(context, queue_name):
                raise InvalidQueueNameError(queue_name)

            datalist = []
            datalist = make_capability_from_lpoptions(context, queue_name)

            current_app.logger.debug((request, datalist))
            return jsonify(datalist)

        except Exception as e:
            current_app.logger.exception(e)
            return exc_to_http_ret(e)


class PrintSetting(Resource):
    def post(self, queue_name: str):
        try:
            context = Context()

            if not is_valid_queue(context, queue_name):
                raise InvalidQueueNameError(queue_name)

            print_setting = request.get_json()

            current_app.logger.debug((request, print_setting))

            capability = make_capability_from_lpoptions(context, queue_name)
            print_setting = validate_setting(print_setting, capability)

            if 'error_code' in print_setting:
                return {'message': print_setting['error_message']}, print_setting['error_code']
            
            else:
                optionlist = []

                for k, v in print_setting.items():
                    # Since the key 'PageSize' is only supported by CW-C6000A_C6500A_Series,CW-C6000P_C6500P_Series,
                    # Other models have to be replaced with 'media' instead.
                    if k == 'PageSize':
                        if not is_pagesize_model_id(context, queue_name):
                            k = 'media'

                    if type(v) is str:
                        optionlist.append(k + '=' + v)
                    elif type(v) is bool:
                        if v:
                            optionlist.append(k + '=' + 'True')
                        else:
                            optionlist.append(k + '=' + 'False')
                    elif type(v) is dict:
                        if v.keys() >= {'CustomWidth', 'CustomHeight'}:
                            custom_value = ('Custom.{0}x{1}mm'.format(
                                v['CustomWidth'], v['CustomHeight']))
                            optionlist.append(k + '=' + custom_value)
                    else:
                        optionlist.append(k + '=' + str(v))

                # DEBUG
                # print(optionlist)

                arg = sum(map(lambda x: ['-o', x], optionlist), [])

                # DEBUG
                # print(arg)

                cmd = ['lpoptions', '-p', queue_name] + arg
                current_app.logger.debug(cmd)
                cp = subprocess.run(cmd, stdout=subprocess.PIPE)
                cp_str = cp.stdout.decode('utf-8')
                _ = cp_str.split(sep='\n')

        except Exception as e:
            current_app.logger.exception(e)
            return exc_to_http_ret(e)

        # Respose Data as same as Get PrintCapability API
        try:
            # Respose Data
            datalist = make_capability_from_lpoptions(context, queue_name)
            return jsonify(datalist)

        except Exception as e:
            current_app.logger.exception(e)
            return exc_to_http_ret(e)


class PrinterCapability(Resource):
    def get(self, queue_name: str):
        try:
            context = Context()

            if not is_valid_queue(context, queue_name):
                raise InvalidQueueNameError(queue_name)

            ret = make_capability_from_elpu(context, queue_name)

            current_app.logger.debug((request, ret))
            return jsonify(ret)

        except Exception as e:
            current_app.logger.exception(e)
            return exc_to_http_ret(e)


class PrinterSetting(Resource):
    def post(self, queue_name: str):
        try:
            context = Context()

            if not is_valid_queue(context, queue_name):
                raise InvalidQueueNameError(queue_name)

            printer_setting = request.get_json(force=True)
            # DEBUG
            # print(printer_setting)

            current_app.logger.debug((request, printer_setting))

            capability = make_capability_from_elpu(
                context, queue_name, with_currentvalue=False)
            printer_setting = validate_setting(printer_setting, capability)

            if 'error_code' in printer_setting:
                return {'message': printer_setting['error_message']}, printer_setting['error_code']
            
            else:

                optionlist = []
                option_names = []

                command_conversions = get_command_conversions(context, queue_name)

                # supported_option_list = ['PaperSource', 'paperShape', 'paperForm', 'formDetectionType', 'formGap', 'printQuality', 'cutPosition', 'printPositionV', 'printPositionH']
                for k, v in printer_setting.items():
                    if type(v) is str:

                        cmd_comb = command_conversions['command_combinations'].get(
                            k)

                        if cmd_comb:
                            for opt_k, opt_v in cmd_comb[v].items():
                                optionlist.append(opt_k + '=' + opt_v)

                            option_names.append(k)
                        else:
                            optionlist.append(k + '=' + v)
                            option_names.append(k)
                    elif type(v) is bool:
                        if k:
                            optionlist.append(k + '=' + 'True')
                            option_names.append(k)
                        else:
                            optionlist.append(k + '=' + 'False')
                            option_names.append(k)
                    else:
                        # mm to dot
                        if k in ['formGap', 'cutPosition', 'printPositionH', 'printPositionV', 'sideMargin', 'rightMargin', 'edgeHole', 'peelPositionA', 'peelPositionB']:
                            optionlist.append(
                                k + '=' + str(len_to_dot(float(v))))
                            option_names.append(k)
                        else:
                            optionlist.append(k + '=' + str(v))
                            option_names.append(k)

                required_procs = command_conversions.get(
                    'required_hardcoded_processes')
                if required_procs and 'append_sidemargin_option_implicitly' in required_procs:
                    append_sidemargin_option_implicitly(optionlist)

                # DEBUG
                # print(optionlist)
                arg = sum(map(lambda x: ['-o', x], optionlist), [])

                # Same as printer capability
                # DEBUG -n drymode
                # param = ['-p', queue_name, '-n']
                param = ['-p', queue_name]

                # DEBUG
                # print(cmd)

                cp = run_printer_utl(param + arg)
                _ = cp.stdout.decode('utf-8')

                # Respose Data as same as Get PrinterCapability API
                capability = make_capability_from_elpu(context, queue_name)
                return jsonify(capability)

        except Exception as e:
            current_app.logger.exception(e)
            return exc_to_http_ret(e)


class Print(Resource):
    def post(self, queue_name: str):
        try:
            context = Context()

            if not is_valid_queue(context, queue_name):
                raise InvalidQueueNameError(queue_name)

            jsondata = request.get_json()
            mimetype = jsondata['mime-type']
            copies = jsondata.get('copies', 1)

            b64encdata = re.sub('^data:.+;base64,', '', jsondata['image'])
            data = base64.b64decode(b64encdata.encode())

            with tempfile.NamedTemporaryFile(suffix=mimetypes.guess_extension(mimetype)) as f:
                f.write(data)
                f.flush()
                lines = ''
                if os.path.getsize(f.name) <= 10485760:
                    # cp = subprocess.run(['lp', '-d', queue_name, f.name], stdout=subprocess.PIPE)
                    cmd = [
                        'lp',
                        '-d', queue_name,
                        '-n', str(copies),
                        f.name
                    ]
                    current_app.logger.debug(cmd)
                    cp = subprocess.run(cmd, stdout=subprocess.PIPE)
                    cp_str = cp.stdout.decode('utf-8')
                    lines = cp_str.split(sep='\n')
                else:
                    raise RequestDataTooLarge()

                lines = list(filter(lambda a: a != '', lines))
                data = {'res': lines}

            return jsonify(data)

        except Exception as e:
            current_app.logger.exception(e)
            return exc_to_http_ret(e)


class Info(Resource):
    def get(self, queue_name: str):
        try:
            context = Context()

            data = get_printer_info(context, queue_name)

            current_app.logger.debug((request, data))
            return jsonify(data)

        except Exception as e:
            current_app.logger.exception(e)
            return exc_to_http_ret(e)


class Status(Resource):
    def get(self, queue_name: str):
        try:
            context = Context()

            if not is_valid_queue(context, queue_name):
                raise InvalidQueueNameError(queue_name)

            data = get_printer_status(context, queue_name)

            current_app.logger.debug((request, data))
            return jsonify(data)

        except Exception as e:
            current_app.logger.exception(e)
            return exc_to_http_ret(e)


class SendCommand(Resource):
    def post(self, queue_name: str):
        try:
            context = Context()

            if not is_valid_queue(context, queue_name):
                raise InvalidQueueNameError(queue_name)

            jsondata = request.get_json()
            current_app.logger.debug((request, jsondata))

            b64encdata = re.sub('^data:.+;base64,', '', jsondata['command'])
            command = base64.b64decode(b64encdata.encode())

            requires_response = jsondata.get('requiresResponse', False)

            if len(command) > 4096:
                raise RequestDataTooLarge()

            with tempfile.NamedTemporaryFile() as cmd_f, tempfile.NamedTemporaryFile() as res_f:
                cmd_f.write(command)
                cmd_f.flush()

                arg = [
                    '-c',
                    '-i', cmd_f.name,
                ] + (['-u', res_f.name] if requires_response else [])

                param = ['-p', queue_name]

                cp = run_printer_utl(param + arg)

                res = res_f.read()
                b64data = base64.b64encode(res).decode('utf-8')

                return jsonify(b64data)

        except Exception as e:
            current_app.logger.exception(e)
            return exc_to_http_ret(e)


class Cancel(Resource):
    def get(self, queue_name: str):
        try:
            context = Context()

            if not is_valid_queue(context, queue_name):
                raise InvalidQueueNameError(queue_name)

            cmd = ['cancel', '-a', queue_name]
            current_app.logger.debug(cmd)
            cp = subprocess.run(cmd, stdout=subprocess.PIPE)
            cp_str = cp.stdout.decode('utf-8')

            if not cp_str:
                return jsonify('All job in the queue {} has been cancelled.'.format(queue_name))
            else:
                return jsonify(cp_str)

        except Exception as e:
            current_app.logger.exception(e)
            return exc_to_http_ret(e)


api = Api(api_bp)
api.add_resource(List, BASE_PATH + '/list')
api.add_resource(PrintCapability, BASE_PATH +
                 '/<string:queue_name>/print/capability')
api.add_resource(PrintSetting, BASE_PATH +
                 '/<string:queue_name>/print/setting')
api.add_resource(Print, BASE_PATH + '/<string:queue_name>/print')
api.add_resource(Cancel, BASE_PATH + '/<string:queue_name>/print/cancel')
api.add_resource(PrinterCapability, BASE_PATH +
                 '/<string:queue_name>/printer/capability')
api.add_resource(PrinterSetting, BASE_PATH +
                 '/<string:queue_name>/printer/setting')
api.add_resource(Info, BASE_PATH + '/<string:queue_name>/printer/info')
api.add_resource(Status, BASE_PATH + '/<string:queue_name>/printer/status')
api.add_resource(SendCommand, BASE_PATH +
                 '/<string:queue_name>/printer/sendcommand')

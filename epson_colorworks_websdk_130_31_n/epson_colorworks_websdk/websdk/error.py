#
# Epson Label Printer Web SDK
#
# Created by Seiko Epson Corporation on 2021/9/8.
# Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
#

from typing import Tuple, Dict


class SDKError(Exception):
    @property
    def code(self) -> int:
        return 500


class SetParamError(SDKError):
    @property
    def code(self) -> int:
        return 501

    def __init__(self, key:str, value:str):
        self.key = key
        self.value = value

    def __str__(self):
        return "{} is unavailable for {}.".format(self.value, self.key)


class InternalServerError(SDKError):
    @property
    def code(self) -> int:
        return 500

    def __str__(self):
        return "Internal server error."


class PrinterNotConnectedError(SDKError):
    @property
    def code(self) -> int:
        return 404

    def __str__(self):
        return "Printer not connected."


class InvalidQueueNameError(SDKError):
    @property
    def code(self) -> int:
        return 400

    def __init__(self, queue_name: str):
        self.queue_name = queue_name

    def __str__(self):
        return "Invalid queue name {}.".format(self.queue_name)
        
class  RequestDataTooLarge(SDKError):
    @property
    def code(self) -> int:
        return 413

    def __str__(self):
        return "Print data is too large. Please send the data below 10 MB."

def exc_to_http_ret(exc: Exception) -> Tuple[Dict[str, str], int]:
    code = exc.code if isinstance(exc, SDKError) else 500

    return {'message': str(exc)}, code

#
# Epson Label Printer Web SDK
#
# Created by Seiko Epson Corporation on 2021/9/8.
# Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
#

wsgi_app = 'sdk:app'

workers = 1
bind = '0.0.0.0:3000'
loglevel = 'debug'
errorlog = 'sdk.log'

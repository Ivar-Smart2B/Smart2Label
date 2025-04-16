# How to Setup Web Application SDK for Epson ColorWorks

## Open Source Software

This software utilizes open source software which is described in requirements.txt for working.
Since these lincenses are applied only to the described versions, the user of this software must check the licenses of the actually used version of open source software.

## Requirements

* Ubuntu 20.04 or later / CentOS 7 or later

## Steps to setup printer driver

1. Install CUPS as root user

Ubuntu:
```console
# apt install cups libcupsimage2
```

CentOS:
```console
# yum install cups
```

2. Download and install the printer driver and utility for the product.

Epson Business System Products Technical Support:

https://download.epson-biz.com/modules/colorworks/

3. Create a printer queue as a root user

Example:
```console
# lpadmin -p QUEUE_NAME -v ipp://IP_ADDRESS/ipp/print -P PPD_PATH -E
```

## Steps to setup SDK

1. Install Python3 and pip as a root user

Ubuntu:
```console
# apt install python3 python3-pip
```

CentOS:
```console
# yum install python3 python3-pip
```

2. Install the required packages using pip with `requirements.txt`

```console
# pip3 install -r requirements.txt
```

3. Move to the `websdk` (directory) located under the path where you expanded the SDK (package).
4. In Gunicorn (program) installed in the step above, start up the SDK together with `gunicorn.conf.py` (settings file).

```console
$ gunicorn -c gunicorn.conf.py
```

By default, SDK listens on port 3000. If you want to change the listening port, please modify `bind` in `gunicorn.conf.py`.
In this example, Gunicorn runs as foreground process. For further usage, please refer to Gunicorn's documents.

### NOTE

* From a security perspective, the SDK is prevented from starting as a root user's process. If you want to start the SDK as a root user's process, please modify the sdk.py script at your own liability.

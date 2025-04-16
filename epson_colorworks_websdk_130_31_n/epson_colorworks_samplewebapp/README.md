# Sample Web App

This is a sample web application for Web Application SDK for Epson ColorWorks.

## Open Source Software

This software utilizes open source software which is described in package.json for working.
Since these lincenses are applied only to the described versions, the user of this software must check the licenses of the actually used version of open source software.

## Requirements

This document describes a web application based on Ubuntu 20.04.

[For building]

* npm

[For serving app]

* Nginx

However, any other web server can be used.

## Steps to build 

1. Install npm with the following command.
```console
# apt install npm
```
2. Change the directory to this WebApp directory on the terminal.
3. Install the required packages written in package.json using the following command.
```console
$ npm install
```
4. Build the files to be served from the web server using following command. 
```console
$ npm run build
```
The built files are created under the `dist` directory. Under this directory, `index.html` and other required files/directories are located.

## Steps to serve

This document describes a web application based on the Nginx web server.

1. Install Nginx using following command. 

```console
# apt install nginx
```

2. Change the web server settings so that requests to the URI `/api/` are passed to the Web Application SDK for Epson ColorWorks server and port (the port is 3000 by default).

Example of Nginx settings (/etc/nginx/nginx.conf) :
```
# When Web Application SDK for Epson ColorWorks server is
# Address: SDK_ADDR
# Port: 3000

http {
    ...
    server {
        ...
        location /api/ {
            proxy_pass http://SDK_ADDR:3000;
        }
    }
}
```

e.g.) If this Nginx server address is `ADDRESS`, the request to Nginx server:

`http://ADDRESS/api/v1/printers/list`

is passed as:

`http://SDK_ADDR:3000/api/v1/printers/list`

to Web Application SDK for Epson ColorWorks server with the settings above.

3. Copy all the built files/directories under `dist` directory onto the web server and serve them so that the entry point `index.html` in the built files is accessed by a web browser.

For the example of Nginx, the default public path in Ubuntu 20.04 is:
```
/var/www/html
```

4. Start Nginx with following command:

```console
# nginx
```

5. On a web browser, open the URL to `index.html` which is served by the web server.

For example, if you are on a Linux desktop where the web server is setup and  the listening port is 80, the URL is:
```
http://localhost:80/index.html
```


## Usage

![](docs/printsetting.png)

### Common Control

[Printer Queue]

Used to select the printer queues currently added to the CUPS server. If there is no printer queue, the text "Not found" is shown instead of a selection box.

Using API:
```
[GET]
/api/v1/printers/list
```

[Menu]

Used to select the main functions from:
 - Printer Info
 - Printer Status
 - Printer Setting
 - Print Setting (selected by default)
 - Print
 - Cancel

In response to the selection, the function-specific controls will appear.

### Printer Info

Shows the printer's static information.

Using API:
```
[GET]
/api/v1/printers/{queueName}/printer/info
```

### Printer Status

Shows the printer's current status.

Using API:
```
[GET]
/api/v1/printers/{queueName}/printer/status
```

### Printer Setting

Shows the printer's device settings and is able to change them using the `Set` button.

Using API:
```
[GET]
/api/v1/printers/{queueName}/printer/capability

[POST]
/api/v1/printers/{queueName}/printer/setting
```

### Print Setting

Shows the printer's print settings and is able to change them using the `Set` button.

Using API:
```
[GET]
/api/v1/printers/{queueName}/print/capability

[POST]
/api/v1/printers/{queueName}/print/setting
```

### Print

Requests printing using the `Print` button after choosing the image file (e.g. PDF, JPEG and so on) to be printed using the `Choose File` button.

Using API:
```
[POST]
/api/v1/printers/{queueName}/print
```

# References

This document details all important web resources used for this project.

## Table of Contents

<!-- TOC -->
* [References](#references)
  * [Table of Contents](#table-of-contents)
  * [Nginx](#nginx)
    * [Deploying with Gunicorn](#deploying-with-gunicorn-)
    * [Adding SSL](#adding-ssl-)
<!-- TOC -->

## Nginx

This project is designed to be hosted on nginx. The resources used can be found here:
* [Deploying with Gunicorn](https://docs.gunicorn.org/en/latest/deploy.html)
* [HTTPS Setup](http://nginx.org/en/docs/http/configuring_https_servers.html)

### Deploying with Gunicorn 

There were some modifications made to the `nginx.conf` example. These modifications are listed below:
1. Changed `worker_processes` to be `auto`
2. Changed the `listen` port to `443`
3. Changed `server_name` to be the correct host names
4. Removed `root` line for static files as static files are served by gunicorn
5. Removed `location /` block as it is not needed
6. Changed the `location @proxy_to_app` block to be `location /` as it is the only location block needed
7. Edited the `proxy_pass` line to be `http://127.0.0.1:8000` as that is the port gunicorn is running on
8. Removed the `error_page` line as the error pages are handled by the application
9. Removed the `location = /500.html` block as it is not needed


### Adding SSL 

The resources used to add SSL to the nginx server can be found [here](http://nginx.org/en/docs/http/configuring_https_servers.html).
The following steps were taken to add SSL to the nginx server:
1. Added the `ssl_certificate` and `ssl_certificate_key` lines to the `nginx.conf` file
2. Added the `ssl_protocols` and `ssl_ciphers` lines to the `nginx.conf` file
3. Edit the `listen` line to be `443 ssl`

Note that the SSL certificate and key must be provided by the user. It is recommended to use a certificate system 
such as [Certbot](https://certbot.eff.org/) to generate the certificate and key.

The final `nginx.conf` file can be found [here](https://github.com/Yuki-42/IA3/blob/master/docs/nginx.conf).

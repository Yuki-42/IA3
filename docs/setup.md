# Setup

The following guide will walk you through the setup of this project for an outwards facing deployment. 

## Prerequisites

- Basic Unix command line knowledge (Ubuntu is used throughout the demo)
- Console access to a dedicated linux box (or a VM)
- A domain name pointing to the IP address of the linux box
- A valid SSL certificate for the domain name (cloudflare is used throughout the demo)

## Step 1: Install Requirements

This project uses Python3.12 as the python version. It will not run on anything lower.

Python3.12 is not available in the default repositories. You will need to add the deadsnakes repository:

```bash
sudo add-apt-repository ppa:deadsnakes/ppa;
```

Install python3.12 and pip3:

```bash
sudo apt update;
sudo apt install python3.12 python3.12-pip python3.12-venv;
```

Install the following packages:
```bash
sudo apt install nginx screen git python3.12-venv authbind gunicorn;
```

## Step 2: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/Yuki-42/IA3.git; 
```

## Step 3: Prepare the virtual environment

Create a virtual environment and install the requirements:

```bash
cd IA3/server/;
python3.12 -m venv venv;

source venv/bin/activate;
pip3 install -r requirements.txt;
```

## Step 4: Configure Nginx

Install Nginx:

```bash
sudo apt install nginx apache2-utils;
```

Remove the default configuration:

```bash
sudo rm /etc/nginx/sites-enabled/default;
```

Create authentication file for your site and add a user:
```bash
sudo htpasswd -c /etc/nginx/.passwords admin;
```

Create a new configuration file:

```bash
sudo nano /etc/nginx/sites-available/ia3;
```

Add the following configuration:

```nginx
# IA3
server {
    # use 'listen 80 deferred;' for Linux
    # use 'listen 80 accept_filter=httpready;' for FreeBSD
    listen              443 ssl;

    ssl_certificate     /etc/ssl/dafox.au.crt;
    ssl_certificate_key /etc/ssl/dafox.au.key;
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    client_max_body_size 4G;

    # set the correct host(s) for your site
    server_name ia3.YOURDOMAIN.au;
    
    auth_basic "Site In Development";
    auth_basic_user_file /etc/nginx/.passwords;

    keepalive_timeout 5;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        # we don't want nginx trying to do something clever with
        # redirects, we set the Host: header above already.
        proxy_redirect off;
        proxy_pass http://127.0.0.1:4269;
    }
}
```

Enable the configuration:

```bash
sudo ln -s /etc/nginx/sites-available/ia3 /etc/nginx/sites-enabled/ia3;
```

Edit the Nginx configuration:

```bash
sudo nano /etc/nginx/nginx.conf;
```

Delete the default configuration and replace it with the following
    
```nginx
worker_processes auto;

user nobody nogroup;
# 'user nobody nobody;' for systems with 'nobody' as a group instead
error_log  /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
  worker_connections 1024; # increase if you have lots of clients
  accept_mutex on; # set to 'on' if nginx worker_processes > 1
  # 'use epoll;' to enable for Linux 2.6+
  # 'use kqueue;' to enable for FreeBSD, OSX
}

http {
  include mime.types;
  include /etc/nginx/sites-enabled/*;
  # fallback in case we can't determine a type
  default_type application/octet-stream;
  access_log /var/log/nginx/access.log combined;
  sendfile on;

  client_max_body_size 4G;
}
```

Restart Nginx:

```bash
sudo service nginx restart;
```

## Step 5: Configure the Application

This is currently a work in progress. Please check back later for updates.

## Step 6: Start the Application

Start the application:

```bash
screen -S IA3;  # Recommended to run in a screen session
source venv/bin/activate;
sh start.sh;
```

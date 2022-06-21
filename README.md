# nginx-forward-proxy

## What is this?

The 'nginx-foward-proxy' is a so simple HTTP proxy server using the nginx.
You can easily build a HTTP proxy server using this.

## Try this container

### Requirement packages

- Docker

## Docker installation

Run each command, preferably one by one.

```
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

## How to use

```
$ docker run --rm -d -p 3128:3128 hinata/nginx-forward-proxy:latest
$ curl -x http://127.0.0.1:3128 https://www.google.co.jp
```

## Reservamos usage:

Build Reservamos image with:

```
sudo docker build -t reservamos/nginx-forward-proxy --build-arg DEFAULT_USER="user" --build-arg DEFAULT_PASSWORD="password" .
```

Run Reservamos container with:

```
sudo docker run --rm -d -p 9501:3128 reservamos/nginx-forward-proxy:latest
```

Preferably to add the following statement to the OS cron jobs to execute the restart_nginx.py script every 15 minutes, and visualize some log messages from restar_nginx_logs.txt:

```
*/15 * * * * /usr/bin/env python3 /home/ubuntu/nginx-forward-proxy/restart_nginx.py >> /home/ubuntu/nginx-forward-proxy/restart_nginx_logs.txt
```


## See also

- https://github.com/chobits/ngx_http_proxy_connect_module

## LICENSE

Apache 2.0

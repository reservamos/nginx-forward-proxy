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

## Deploy on AWS Lightsail

- Access AWS and search for Lightsail
- Create a LightSail instance

<img src="https://user-images.githubusercontent.com/99829334/220213067-9d20b112-98af-4b23-87c8-8a7e1af010bb.png">

- Select Linux/Unix platform
- Select OS only blueprint with Ubuntu 20.04
- Selected the 3.5 USD per month plan
- The name was saas-proxy

<img src="https://user-images.githubusercontent.com/99829334/220213101-1e97e057-e8b5-4a8f-836c-620e85761b3b.png">

- Then: create instance
- When creating the instance, I selected Connect using ssh, which opens a tab to execute the commands in the project's readme, from installation to reserved usage, but the Docker installation is only done the first time, the others would be every time the server is restarted.

<img src="https://user-images.githubusercontent.com/99829334/220212818-30ec6218-e725-46ae-9acd-de27105a84ea.png">

- Configure the instance with a static IP, so that even if the server is restarted, it continues with the same IP.

<img src="https://user-images.githubusercontent.com/99829334/220213160-34670b14-034b-4212-ba69-e54e159d6104.png">

- For security reasons, the rules were changed so that the port is 9501.

<img src="https://user-images.githubusercontent.com/99829334/220214007-4df152f8-021d-4a68-acf5-0be65ba37158.png">

- I cloned the project inside the instance and then executed the reserved usage command, and it seems to be working fine! (Still need to create a startup script because it gets misconfigured every time the server is restarted).

<img src="https://user-images.githubusercontent.com/99829334/220213257-d67e1bf2-7c5e-4a15-b1ef-543758555aae.png">

- Create a startup script (https://www.youtube.com/watch?v=-aKb-k8B8xo) on the server that executes the sh:

```
[Unit]
Description=Startup script

[Service]
ExecStart=/bin/bash /home/ubuntu/StartScript.sh

[Install]
WantedBy=multi-user.target
```

- Create ssh (https://platzi.com/tutoriales/1468-bash-shell/9694-como-crear-un-shell-script-en-linuxunix/?utm_source=google&utm_medium=cpc&utm_campaign=19643931773&utm_adgroup=&utm_content=&gclid=Cj0KCQiAorKfBhC0ARIsAHDzsltAzRH3G9xmNRcji-WjhbxmacraIzrGgI8knxC9i-74UBPF6-ubI_0aAhAeEALw_wcB&gclsrc=aw.ds):

```
cd nginx-forward-proxy
sudo docker build -t reservamos/nginx-forward-proxy --build-arg DEFAULT_USER="<INSERT_USER>" --build-arg DEFAULT_PASSWORD="<INSERT_PASSWORD>" .
sudo docker run --rm -d -p 9501:3128 reservamos/nginx-forward-proxy:latest
```

Restart server and run the next command on the terminal

```
curl -x http://#{Poner IP estática}:9501 https://www.google.co.jp
```

Should return a correct result.

## Some Docker commands

```
sudo docker ps -a
sudo docker logs -f 3e81e49039ff

sudo systemctl stop docker
sudo systemctl start docker
```

## See also

- https://github.com/chobits/ngx_http_proxy_connect_module

## LICENSE

Apache 2.0

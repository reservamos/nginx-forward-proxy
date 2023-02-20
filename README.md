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

- Acceder a AWS y buscar Lightsail
- Crear una instancia de LightSail
- You are creating this instance in Ohio, Zone A (us-east-2a)
- En select a platform linux/unix
- Select a blueprint OS only con Ubuntu 20.04
- Se seleccionó el plan de 3.5 USD al mes
- El name fue saas-proxy
- Luego: crear instancia
- Al crear la instancia, le di Connect using ssh, el cual abre una pestaña para ejecutar los comandos que están en el read me del proyecto, desde la instalación hasta el reservamos usage, pero el de instalar Docker solo es la primera vez, los otros serían cada que se reinicie el server.
- Configurar la instancia con IP estática, para que aunque se reinicie el server, continúe con la misma IP
- Cloné el proyecto dentro de la instancia y luego ejecuté el reservamos usage y al parecer ya está funcionando bien! (Aun falta crear un startup script, porque se desconfigura cada que reiniciamos el server)
- Crear un script startup (https://www.youtube.com/watch?v=-aKb-k8B8xo) en el server que ejecute el sh

```
[Unit]
Description=Startup script

[Service]
ExecStart=/bin/bash /home/ubuntu/StartScript.sh

[Install]
WantedBy=multi-user.target
```

- Creé el sh (https://platzi.com/tutoriales/1468-bash-shell/9694-como-crear-un-shell-script-en-linuxunix/?utm_source=google&utm_medium=cpc&utm_campaign=19643931773&utm_adgroup=&utm_content=&gclid=Cj0KCQiAorKfBhC0ARIsAHDzsltAzRH3G9xmNRcji-WjhbxmacraIzrGgI8knxC9i-74UBPF6-ubI_0aAhAeEALw_wcB&gclsrc=aw.ds):

```
echo "ingresando al proyecto proxy"
cd nginx-forward-proxy

echo "docker build a reservamos nginx-forward-proxy"
sudo docker build -t reservamos/nginx-forward-proxy --build-arg DEFAULT_USER="<INSERT_USER>" --build-arg DEFAULT_PASSWORD="<INSERT_PASSWORD>" .
echo "docker run a nginx-forward-proxy"
sudo docker run --rm -d -p 9501:3128 reservamos/nginx-forward-proxy:latest
```

Y reiniciamos el server, una vez reiniciado si está todo Ok, al correr el siguiente comando desde nuestra terminal:

curl -x http://#{Poner IP estática}:9501 https://www.google.co.jp

Nos debe de devolver un resultado correcto.

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

### Desenvolvendo localmente:

Para desenvolver o backend do projeto, recomenda-se utilizar o [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html#via-pip), 
com o virtualenv instalado, crie um ambiente isolado em Python com o seguinte comando:

`$ virtualenv ~/envs/websocket -p python3.8`

Em seguida ative-o:

`$ source ~/envs/websocket/bin/activate`

E instale os pacotes requeridos:

`$ make dev-env`

### TODO: Encontrar um solução de sticky session no LB da AWS

https://docs.docker.com/engine/swarm/ingress/

#### Criando Serviço:

1. `$ sudo nano $HOME/.ngrok2/ngrok.yml`
2. 
```
authtoken: 6yMXA63qefMZqCWSCHaaYq_5LufcciP1rG4LCZETjC6V
tunnels:
  first:
    addr: 3002
    proto: http    
  second:
    addr: 8080
    proto: http
```
3. `$ ./ngrok start first second`
4. Get server side address and replace it at index.html for the `backendHost`
5. `$ docker-compose up`
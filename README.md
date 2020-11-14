### Desenvolvendo localmente:

Para desenvolver o backend do projeto, recomenda-se utilizar o [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html#via-pip), 
com o virtualenv instalado, crie um ambiente isolado em Python com o seguinte comando:

`$ virtualenv ~/envs/websocket -p python3.8`

Em seguida ative-o:

`$ source ~/envs/websocket/bin/activate`

E instale os pacotes requeridos:

`$ make dev-env`
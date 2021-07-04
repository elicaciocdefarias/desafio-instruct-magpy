# MagPy

API REST criada para gerenciar projetos escritos com python e seus pacotes.

O principal motivo para desenvolvimento dessa ferramento foi poder centralizar o gerenciamento dos pacotes usados nos projetos.

## Objetivo
Garantir que os projetos estão usando as últimas versões disponíves dos pacotes.

## Principais Tecnologias utilizadas
* Python = "3.9.5"
* django = "~=3.2"
* djangorestframework = "~=3.12"
* requests = "~=2.25"
* gunicorn = "~=20.1"
* psycopg2 = "~=2.9"
* whitenoise = "~=5.2"

## Demostração

Click [aqui](https://magpy-elicacio.herokuapp.com/swagger-ui/) para acessar.

## Como instalar localmente

Clone o projeto
```
git clone https://github.com/elicaciocdefarias/teste-python-jr-remoto-2021-06.git
```

Acesse o projeto
```
cd teste-python-jr-remoto-2021-06
```

Crie o arquivo .env na raiz do projeto e adicione as duas variáveis abaixo
```
SECRET_KEY=altere_esse_valor
DEBUG=True
```

Instale todas as dependências para o seu projeto
```
pipenv install --dev
```

Rode as migrações
```
pipenv run python manage.py migrate
```

Para rodar os testes de unidade
```
pipenv run pytest -vv
```

Para rodar os testes de integração
> **Observações:**
>
> Antes de prosseguir você precisa instalar [k6](https://k6.io), click [aqui](https://k6.io/docs/getting-started/installation/), para acessar o guia de instalação.

Abra duas janelas do terminal.
> **Observações:**
>
> Se estiver usando [tilix](https://gnunn1.github.io/tilix-web/) ou [tmux](https://github.com/tmux/tmux/wiki), basta dividir a janela em dois paineis.

Em uma janela ou painel, rode o comando abaixo para subir a aplicação.
```
pipenv run python manage.py runserver
```

Na outra, rode.
```
k6 run -e API_BASE='http://127.0.0.1:8000/' tests-open.js
```

## Mode de usar

> **Observações**
>
> Os exemplos abaixo foram realizados usando [HTTPie](https://httpie.io/) 

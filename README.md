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
```bash
git clone https://github.com/elicaciocdefarias/teste-python-jr-remoto-2021-06.git
```

Acesse o projeto
```bash
cd teste-python-jr-remoto-2021-06
```

Crie o arquivo .env na raiz do projeto e adicione as duas variáveis abaixo
```env
SECRET_KEY=altere_esse_valor
DEBUG=True
```

Instale todas as dependências, incluindo as de desenvolvimento
```bash
pipenv install --dev
```

Rode as migrações
```bash
pipenv run python manage.py migrate
```

Para rodar os testes de unidade
```bash
pipenv run pytest -vv
```

Para rodar os testes de integração
> **Observações:**
>
> Antes de prosseguir você precisa instalar [k6](https://k6.io), click [aqui](https://k6.io/docs/getting-started/installation/) para acessar o guia de instalação.

Abra duas janelas do terminal.
> **Observações:**
>
> Se estiver usando [tilix](https://gnunn1.github.io/tilix-web/) ou [tmux](https://github.com/tmux/tmux/wiki), basta dividir a janela em dois paineis.

Em uma janela ou painel, rode o comando abaixo para subir a aplicação.
```bash
pipenv run python manage.py runserver
```

Na outra janela ou painel, rode.
```bash
k6 run -e API_BASE='http://127.0.0.1:8000/' tests-open.js
```

> **Observações:**
>
> Rode o comando abaixo para testar a aplicação em produção.
```bash
k6 run -e API_BASE='https://magpy-elicacio.herokuapp.com' tests-open.js
```

## Mode de usar

> **Observações**
>
> Os exemplos abaixo foram realizados usando [HTTPie](https://httpie.io/).

### Principais operações

#### Criar
```bash
http POST 'http://127.0.0.1:8000/api/projects/' name='borg' packages:='[]' 
```

Retorno com sucesso.
```json
{
    "name": "borg",
    "packages": []
}
```

Retorno com falha.
```json
{
    "name": [
        "project with this name already exists."
    ]
}
```

#### Criar com pacotes
```bash
http POST 'http://127.0.0.1:8000/api/projects/' name='dinos' packages:='[{"Django": "3.2.5"}]' 
```

Retorno com sucesso.
```json
{
    "name": "dinos",
    "packages": [
        {
            "name": "Django",
            "version": "3.2.5"
        }
    ]
}
```

Retorno com falha.
```json
{
    "error": "One or more packages doesn't exist"
}
```


#### Listar todos.
```bash
http GET 'http://127.0.0.1:8000/api/projects/'
```

Retorno com resultados.
```json
[
    {
        "name": "borg",
        "packages": []
    },
    {
        "name": "dinos",
        "packages": [
            {
                "name": "Django",
                "version": "3.2.5"
            }
        ]
    }
]
```
Retorno sem resultados.
```json
[]
```

>**Observações**
>
>As operações abaixo são realizadas usando o nome do projeto.
>
>Está sendo usado o nome do projeto criado [aqui](####Criar)

#### Listar um.
```bash
http GET 'http://127.0.0.1:8000/api/projects/borg/'
```
Retorno com sucesso.
```json
{
    "name": "borg",
    "packages": []
}
```
Retorno com falha.
```json
{
    "detail": "Not found."
}
```
#### Atualizar um.
```bash
http PUT 'http://127.0.0.1:8000/api/projects/borg/'
```
Retorno com sucesso.
```json
{
    "name": "borg",
    "packages": []
}
```
Retorno com falha.
```json
{
    "detail": "Not found."
}
```
#### Deletar um.
```bash
http DELETE 'http://127.0.0.1:8000/api/projects/borg/'
```

Retorno com sucesso.
```json

```
Retorno com falha.
```json
{
    "detail": "Not found."
}
```
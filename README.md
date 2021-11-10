# mercadinho-voinha [WIP]
Sistema de supermercado desenvolvido utilizando arquitetura de microsserviços, para a disciplina de Arquitetura de Sistemas Orientado a Serviços ministrada no semestre 2020.2 na UFRPE.

## Arquitetura proposta

### Modelagem
Para entender mais sobre a arquitetura proposta, veja a figura a baixo.

![arquitetura-proposta](docs/arquitetura.png)

### Tecnologias

* O API Gateway será desenvolvido utilizando o [Kong](https://konghq.com/);
* Os microsserviços serão desenvolvidos utilizando REST, com o [FastAPI](https://fastapi.tiangolo.com/);
* A linguagem principal de desenvolvimento será o Python;
* Para versionamento dos pacotes Python, será utilizado o [Poetry](https://python-poetry.org/);
* Documentação será disponibilizada via [Swagger](https://swagger.io/);
* A comunicação com banco de dados relacional será via [SQLAlchemy](https://www.sqlalchemy.org/);
* Irá ser utilizado como banco de dados o [PostgreSQL](https://www.postgresql.org/).

## Instalação

### Banco de Dados

Para criar o banco de dados que será utilizado nesse projeto, antes você precisa instalar o PostgreSQL:

```bash
docker pull postgres:14
docker volume create postgres-volume
docker run --rm -d --name=postgres14 -p 5432:5432 -v postgres-volume:/var/lib/postgresql/data -e POSTGRES_PASSWORD=[your_password] postgres
```

> Para mais detalhes sobre os passos realizados, acesse o [link](https://linuxiac.com/postgresql-docker/)

### Configuração do Banco de Dados

Para configurar o banco de dados, execute na raiz do projeto em seu terminal:

```bash
./db_config.sh
```

## Execução

TODO

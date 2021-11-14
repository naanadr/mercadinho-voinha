# ProdutosAPI

## Instalação

```bash
poetry install
poetry shell
```

## Execução

Crie um arquivo `.env` com os mesmos campos contidos no [`.env_example`](/.env_example). Esse deverá ser as informações cadastradas do UsuárioEstoquista do Banco de Dados.

> Verifique se o banco de dados está em execução

Para executar a API, execute o seguinte comando:
```bash
uvicorn app.main:app --reload
```

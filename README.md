# Fast_zero

Tecnologias usadas neste projeto de estudo:
- python
- fastapi
- poetry
- sqlite
- sqlalchemy
- alembic
- pytest

## Usando o Alembic para migrações

Iniciar o Alembic em um projeto

```shell
alembic init migrations
```

Para gerar uma migração:

```shell
alembic revision --autogenerate -m "<DAR_NOME_PARA_A_MIGRACAO"
```

## Acessando o banco via terminal e seus comandos

```shell
sqlite3 database.db
.schema
select version_num from alembic_version;
.quit
```

## Aplicando todas as migrações não aplicadaas com o Alembic

```shell
alembic upgrade head
```

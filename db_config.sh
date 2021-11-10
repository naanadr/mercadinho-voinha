#!/bin/bash

#Set the value of variable
database="db_mercadinho"
psqlUser="admin_mercadinho"
password="super_senha"

echo "------ Drop and Create DATABASE ------"
docker exec -it postgres14 psql -U postgres -c "DROP DATABASE IF EXISTS db_mercadinho"
docker exec -it postgres14 psql -U postgres -T template1 -c "CREATE DATABASE db_mercadinho"

echo "------ Drop and Create ROLES ------"
docker exec -it postgres14 psql -U postgres -d $database -c "DROP ROLE IF EXISTS admin_mercadinho"
docker exec -it postgres14 psql -U postgres -d $database -c "CREATE ROLE admin_mercadinho SUPERUSER NOCREATEDB CREATEROLE NOINHERIT LOGIN PASSWORD 'super_senha'"

docker exec -it postgres14 psql -U postgres -d $database -c "DROP ROLE IF EXISTS user_rh"
docker exec -it postgres14 psql -U postgres -d $database -c "CREATE ROLE user_rh NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN PASSWORD 'userrhpwd';
GRANT INSERT ON TABLE public.tb_funcionarios TO user_rh;
GRANT SELECT ON TABLE public.tb_funcionarios TO user_rh;"

docker exec -it postgres14 psql -U postgres -d $database -c "DROP ROLE IF EXISTS user_rh"
docker exec -it postgres14 psql -U postgres -d $database -c "CREATE ROLE user_cliente NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOLOGIN;
GRANT SELECT ON TABLE public.tb_pedido TO user_cliente;
GRANT SELECT ON TABLE public.tb_estoque TO user_cliente;
GRANT SELECT ON TABLE public.tb_produto TO user_cliente;
GRANT INSERT ON TABLE public.tb_pedido TO user_cliente;"

docker exec -it postgres14 psql -U postgres -d $database -c "DROP ROLE IF EXISTS user_estoquista"
docker exec -it postgres14 psql -U postgres -d $database -c "CREATE ROLE user_estoquista NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN PASSWORD 'readonlypwd';
GRANT SELECT ON TABLE public.tb_estoque TO user_estoquista;
GRANT INSERT ON TABLE public.tb_estoque TO user_estoquista;
GRANT SELECT ON TABLE public.tb_pedido TO user_estoquista;
GRANT SELECT ON TABLE public.tb_produto TO user_estoquista;
GRANT INSERT ON TABLE public.tb_produto TO user_estoquista;"

echo "------ Drop and create TABLES ------"
docker exec -it postgres14 psql -U $psqlUser -d $database -c "DROP TABLE IF EXISTS public.tb_funcionarios"
docker exec -it postgres14 psql -U $psqlUser -d $database -c "CREATE TABLE public.tb_funcionarios (
	id bigint GENERATED ALWAYS AS IDENTITY,
  cpf varchar NOT NULL,
	nome varchar NOT NULL,
  dt_nascimento date NOT NULL,
	setor varchar NOT NULL,
  cargo varchar NOT NULL,
  is_ativo bool NOT NULL,
	dt_entrada date NOT NULL,
	dt_desligamento date NOT NULL,
	dt_atualizacao date NOT NULL
)"

docker exec -it postgres14 psql -U $psqlUser -d $database -c "DROP TABLE IF EXISTS public.tb_produto"
docker exec -it postgres14 psql -U $psqlUser -d $database -c "CREATE TABLE public.tb_produto (
	id bigint GENERATED ALWAYS AS IDENTITY,
	nome varchar NOT NULL,
	is_perecivel boolean NOT null,
	PRIMARY KEY (nome),
	UNIQUE (id)
)"

docker exec -it postgres14 psql -U $psqlUser -d $database -c "DROP TABLE IF EXISTS public.tb_estoque"
docker exec -it postgres14 psql -U $psqlUser -d $database -c "CREATE TABLE public.tb_estoque (
	id bigint GENERATED ALWAYS AS IDENTITY,
	dt_cadastro date NOT NULL,
	id_produto bigint NOT NULL,
	qt_estoque int NOT NULL,
	vl_unidade float8 NOT NULL,
	unidade_medida varchar NOT NULL,
	dt_validade date NULL,
  CONSTRAINT fk_produto
    FOREIGN KEY(id_produto)
			REFERENCES tb_produto(id)
)"

docker exec -it postgres14 psql -U $psqlUser -d $database -c "DROP TABLE IF EXISTS public.tb_pedido"
docker exec -it postgres14 psql -U $psqlUser -d $database -c "CREATE TABLE public.tb_pedido (
	id bigint GENERATED ALWAYS AS IDENTITY,
	dt_cadastro date NOT NULL,
	id_produto int NOT NULL,
	qtd_produto int NOT NULL,
	id_pedido int NOT NULL,
	vl_unidade float8 NOT NULL,
	vl_total_produto float8 NOT NULL,
  CONSTRAINT fk_produto
    FOREIGN KEY(id_produto)
			REFERENCES tb_produto(id)
);"

echo "All steps finished!"

#!/bin/bash

#Set the value of variable
export $(grep -v '^#' .env)

echo $database_rh

echo "------ Drop and Create DATABASES ------"
docker exec -it postgres14 psql -U postgres -c "DROP DATABASE IF EXISTS $database_rh"
docker exec -it postgres14 psql -U postgres -T template1 -c "CREATE DATABASE $database_rh"
docker exec -it postgres14 psql -U postgres -c "DROP DATABASE IF EXISTS $database_produtos"
docker exec -it postgres14 psql -U postgres -T template1 -c "CREATE DATABASE $database_produtos"
docker exec -it postgres14 psql -U postgres -c "DROP DATABASE IF EXISTS $database_estoque"
docker exec -it postgres14 psql -U postgres -T template1 -c "CREATE DATABASE $database_estoque"

echo "------ Drop and Create ROLES ------"
docker exec -it postgres14 psql -U postgres -d $database_rh -c "DROP ROLE IF EXISTS $superUser"
docker exec -it postgres14 psql -U postgres -d $database_rh -c "CREATE ROLE $superUser SUPERUSER NOCREATEDB CREATEROLE NOINHERIT LOGIN PASSWORD $superUserPWD"
docker exec -it postgres14 psql -U postgres -d $database_produtos -c "DROP ROLE IF EXISTS $superUser"
docker exec -it postgres14 psql -U postgres -d $database_produtos -c "CREATE ROLE $superUser SUPERUSER NOCREATEDB CREATEROLE NOINHERIT LOGIN PASSWORD $superUserPWD"
docker exec -it postgres14 psql -U postgres -d $database_estoque -c "DROP ROLE IF EXISTS $superUser"
docker exec -it postgres14 psql -U postgres -d $database_estoque -c "CREATE ROLE $superUser SUPERUSER NOCREATEDB CREATEROLE NOINHERIT LOGIN PASSWORD $superUserPWD"

echo "------ Drop and create TABLES ------"
docker exec -it postgres14 psql -U $superUser -d $database_rh -c "DROP TABLE IF EXISTS public.tb_funcionarios"
docker exec -it postgres14 psql -U $superUser -d $database_rh -c "CREATE TABLE public.tb_funcionarios (
	id bigint GENERATED ALWAYS AS IDENTITY,
  cpf varchar NOT NULL,
	nome varchar NOT NULL,
  dt_nascimento date NOT NULL,
	setor varchar NOT NULL,
  cargo varchar NOT NULL,
  is_ativo bool NOT NULL,
	dt_entrada date NOT NULL,
	dt_desligamento date,
	dt_atualizacao date NOT NULL
)"

docker exec -it postgres14 psql -U $superUser -d $database_produtos -c "DROP TABLE IF EXISTS public.tb_produto CASCADE"
docker exec -it postgres14 psql -U $superUser -d $database_produtos -c "CREATE TABLE public.tb_produto (
	id bigint GENERATED ALWAYS AS IDENTITY,
	nome varchar NOT NULL,
	marca varchar NOT NULL,
	is_perecivel boolean NOT null,
	dt_cadastro date NOT NULL,
	PRIMARY KEY (nome, marca),
	UNIQUE (id)
)"

docker exec -it postgres14 psql -U $superUser -d $database_estoque -c "DROP TABLE IF EXISTS public.tb_estoque"
docker exec -it postgres14 psql -U $superUser -d $database_estoque -c "CREATE TABLE public.tb_estoque (
	id bigint GENERATED ALWAYS AS IDENTITY,
	dt_cadastro date NOT NULL,
	id_produto bigint NOT NULL,
	qt_estoque int NOT NULL,
	vl_unidade float8 NOT NULL,
	unidade_medida varchar NOT NULL,
	dt_validade date NULL,
	is_ativo boolean NULL
)"

echo "------ Drop and create USERS ------"
docker exec -it postgres14 psql -U superUser -d $database_rh -c "DROP ROLE IF EXISTS $userAPIRH"
docker exec -it postgres14 psql -U superUser -d $database_rh -c "CREATE ROLE $userAPIRH NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN PASSWORD $userAPIRHPWD;
GRANT INSERT ON TABLE public.tb_funcionarios TO $userAPIRH;
GRANT SELECT ON TABLE public.tb_funcionarios TO $userAPIRH;"

docker exec -it postgres14 psql -U postgres -d $database_produtos -c "DROP ROLE IF EXISTS $userAPIProduto"
docker exec -it postgres14 psql -U postgres -d $database_produtos -c "CREATE ROLE $userAPIProduto NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN PASSWORD $userAPIProdutoPWD;
GRANT SELECT ON TABLE public.tb_produto TO $userAPIProduto;
GRANT INSERT ON TABLE public.tb_produto TO $userAPIProduto;"

docker exec -it postgres14 psql -U postgres -d $database_estoque -c "DROP ROLE IF EXISTS $userAPIEstoque"
docker exec -it postgres14 psql -U postgres -d $database_estoque -c "CREATE ROLE $userAPIEstoque NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN PASSWORD $userAPIEstoquePWD;
GRANT SELECT ON TABLE public.tb_estoque TO $userAPIEstoque;
GRANT INSERT ON TABLE public.tb_estoque TO $userAPIEstoque;
GRANT UPDATE ON TABLE public.tb_estoque TO $userAPIEstoque;"

echo "All steps finished!"

drop database if exists back_db;
create database back_db;
\c back_db;

create table person (
    person_id           varchar(50) primary key,
    name                varchar(100) not null,
    address_id          varchar(50),
    created_at          timestamp default (now())
);

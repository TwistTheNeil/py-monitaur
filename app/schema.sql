drop table if exists servers;
drop table if exists users;

create table servers (
    name text,
    id text primary key
);

create table users (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null
);
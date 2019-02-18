drop table if exists servers;
drop table if exists users;

create table servers (
    name text not null,
    id text primary key
);

create table services (
    name text not null,
    id text primary key
);

create table logged_times (
    id integer primary key autoincrement,
    server_name text,
    service_name text,
    logged_at datetime default current_timestamp not null
);

create table users (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null
);
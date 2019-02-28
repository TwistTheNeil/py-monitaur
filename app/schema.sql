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
    server_id text,
    service_id text,
    logged_at timestamp default (strftime('%s', 'now')) not null,
    foreign key (server_id) references servers(id),
    foreign key (service_id) references services(id)
);

create table users (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null
);
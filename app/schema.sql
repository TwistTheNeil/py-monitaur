drop table if exists servers;
drop table if exists users;

-- Need to set PRAGMA foreign_keys=1

create table servers (
    name text not null,
    enabled integer default 1 not null,
    pinned integer default 0 not null,
    id text primary key
);

create table services (
    name text not null,
    server_id text not null,
    id text primary key,
    enabled integer default 1 not null,
    pinned integer default 0 not null,
    foreign key(server_id) references servers(id) on delete cascade
);

create table logged_times (
    id integer primary key autoincrement,
    server_id text,
    service_id text,
    logged_at integer default (cast(strftime('%s', 'now') as integer)) not null,
    load float,
    foreign key(server_id) references servers(id) on delete cascade,
    foreign key(service_id) references services(id) on delete cascade
);

create table users (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null
);
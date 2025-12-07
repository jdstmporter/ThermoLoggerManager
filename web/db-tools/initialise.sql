create database if not exists AllSaints;

create table if not exists AllSaints.records
(
    seq         int auto_increment
        primary key,
    timestamp   int         not null,
    temperature float       not null,
    humidity    float       not null,
    battery     float       not null,
    mac         varchar(64) not null,
    sensor      varchar(64) not null
);

create table if not exists AllSaints.sensors
(
    mac  varchar(64) not null,
    name varchar(64) not null,
    constraint macs_index
        unique (mac)
);

create user if not exists 'sql'@'localhost' identified by 'sql';
grant all on AllSaints.* to 'sql'@'localhost';




create database if not exists AllSaints;

create table if not exists AllSaints.records
(
    seq         int auto_increment
        primary key,
    timestamp   int         not null,
    temperature float       not null,
    humidity    float       not null,
    battery     float       not null,
    sensor      varchar(32) not null
);

create user if not exists 'sql'@'localhost' identified by 'sql';
grant all on AllSaints.* to 'sql'@'localhost';




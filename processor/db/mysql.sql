create table records
(
    seq         int         not null
        primary key,
    timestamp   float       not null,
    temperature float       not null,
    humidity    float       not null,
    battery     float       not null,
    sensor      varchar(32) not null
);

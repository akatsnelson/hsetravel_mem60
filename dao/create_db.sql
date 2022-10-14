drop table if exists steps_history;
drop table if exists users;
drop table if exists rooms;

create table if not exists steps_history
(
    id        integer
        constraint steps_pk primary key autoincrement,
    curr_step varchar
        constraint check_u_curr_step_nn not null,
    prev_step integer
);

create table if not exists users
(
    tg_id               integer(15)
        constraint users_pk
            primary key,
    username            varchar(100) default "",
    s_1               integer(3) default -1,
    s_2               integer(3) default -1,
    s_3               integer(3) default -1,

    step                integer references steps_history,
    user_freeze         boolean
        constraint u_freeze_nn not null default false

);

create unique index users_tg_id_uindex
    on users (tg_id);


create table email (
    email_id serial primary key,
    email_address varchar2(100),
    email_type varchar2(1) not null,
    person_id int not null
);

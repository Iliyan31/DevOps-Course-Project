create table email (
    email_id serial primary key,
    email_address varchar(100),
    email_type varchar(1) not null,
    person_id int not null
);

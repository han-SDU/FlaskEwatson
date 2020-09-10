create database if not exists db_sensor;
use db_sensor;

#Creates Table for Temperatures
create table if not exists tbl_temperature(
	fld_pk_id int not null auto_increment,
	fld_time timestamp,
	fld_value decimal(5,2) not null,
	primary key(fld_pk_id)
);

#Create Table for Humidity
create table if not exists tbl_humidity(
	fld_pk_id int not null auto_increment,
	fld_time timestamp,
	fld_value decimal(4,2) not null,
	primary key(fld_pk_id)
);

#Create Table for CO2
create table if not exists tbl_co2(
	fld_pk_id int not null auto_increment,
	fld_time timestamp,
	fld_value smallint unsigned not null,
	primary key(fld_pk_id)
);

#Create Table for Pressure
create table if not exists tbl_pressure(
	fld_pk_id int not null auto_increment,
	fld_time timestamp,
	fld_value decimal(5,1) not null,
	primary key(fld_pk_id)
);

#Events event runner must be configured to run
DELIMITER !!
create event if not exists event_cleaning
on schedule every 1 minute
on completion preserve
do
begin
delete from tbl_temperature where datediff(now(),fld_time) > 365;
delete from tbl_humidity where datediff(now(),fld_time) > 365;
delete from tbl_co2 where datediff(now(),fld_time) > 365;
delete from tbl_pressure where datediff(now(),fld_time) > 365;
end!!
DELIMITER ;

#Stored procedures
DELIMITER !!
create procedure if not exists generate_data(in million int)
begin
declare i int default 0;
while i < million do
	select concat("Generating million: ",i+1,"/",million) as "Iteration";
	select "Generating million rows in tbl_humidity" as "Status";
	call generate_million_humidity();
	select "Generating million rows in tbl_temperature" as "Status";
	call generate_million_temperature();
	select "Generating million rows in tbl_temperature" as "Status";
	call generate_million_co2();
	select "Generating million rows in tbl_co2" as "Status";
	call generate_million_pressure();
	set i = i+1;
end while;
end!!
DELIMITER ;

DELIMITER !!
create procedure if not exists generate_million_humidity()
begin
insert into tbl_humidity(fld_time,fld_value)
select now(),rand() from
(
select a.N + b.N *10 + c.N * 100 + d.N * 1000 + e.N * 100000 + f.N * 1000000 +1 N from
(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)a
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)b
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)c
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)d
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)e
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)f
)t;
end!!
DELIMITER ;

DELIMITER !!
create procedure if not exists generate_million_temperature()
begin
insert into tbl_temperature(fld_time,fld_value)
select now(),rand() from
(
select a.N + b.N *10 + c.N * 100 + d.N * 1000 + e.N * 100000 + f.N * 1000000 +1 N from
(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)a
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)b
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)c
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)d
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)e
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)f
)t;
end!!
DELIMITER ;

DELIMITER !!
create procedure if not exists generate_million_co2()
begin
insert into tbl_co2(fld_time,fld_value)
select now(),rand() from
(
select a.N + b.N *10 + c.N * 100 + d.N * 1000 + e.N * 100000 + f.N * 1000000 +1 N from
(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)a
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)b
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)c
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)d
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)e
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)f
)t;
end!!
DELIMITER ;

DELIMITER !!
create procedure if not exists generate_million_pressure()
begin
insert into tbl_pressure(fld_time,fld_value)
select now(),rand() from
(
select a.N + b.N *10 + c.N * 100 + d.N * 1000 + e.N * 100000 + f.N * 1000000 +1 N from
(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)a
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)b
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)c
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)d
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)e
,(select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9)f
)t;
end!!
DELIMITER ;

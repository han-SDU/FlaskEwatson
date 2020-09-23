create database if not exists db_sensor;
use db_sensor;

#Creates Table for Temperatures
create table if not exists tbl_recent_temperature(
	fld_pk_id int not null auto_increment,
	fld_time timestamp not null,
	fld_value decimal(5,2) not null,
	primary key(fld_pk_id)
);

create table if not exists tbl_historic_temperature(
	fld_pk_id int not null auto_increment,
	fld_start_time timestamp not null,
	fld_end_time timestamp not null,
	fld_average decimal(5,2),
	primary key(fld_pk_id)
);

#Create Table for Humidity
create table if not exists tbl_recent_humidity(
	fld_pk_id int not null auto_increment,
	fld_time timestamp not null,
	fld_value decimal(4,2) not null,
	primary key(fld_pk_id)
);

create table if not exists tbl_historic_humidity(
	fld_pk_id int not null auto_increment,
	fld_start_time timestamp not null,
	fld_end_time timestamp not null,
	fld_average decimal(4,2),
	primary key(fld_pk_id)
);

#Create Table for CO2
create table if not exists tbl_recent_co2(
	fld_pk_id int not null auto_increment,
	fld_time timestamp not null,
	fld_value smallint unsigned not null,
	primary key(fld_pk_id)
);

create table if not exists tbl_historic_co2(
	fld_pk_id int not null auto_increment,
	fld_start_time timestamp not null,
	fld_end_time timestamp not null,
	fld_average smallint unsigned,
	primary key(fld_pk_id)
);

#Create Table for Pressure
create table if not exists tbl_recent_pressure(
	fld_pk_id int not null auto_increment,
	fld_time timestamp not null,
	fld_value decimal(5,1) not null,
	primary key(fld_pk_id)
);

create table if not exists tbl_historic_pressure(
	fld_pk_id int not null auto_increment,
	fld_start_time timestamp not null,
	fld_end_time timestamp not null,
	fld_average decimal(5,2),
	primary key(fld_pk_id)
);

DELIMITER !!
create event if not exists ev_clean_recent
on schedule every 1 hour
on completion preserve
do
begin
delete from tbl_recent_temperature where hour(timediff(utc_timeStamp(),fld_time)) > 72;
delete from tbl_recent_humidity where hour(timediff(utc_timeStamp(),fld_time)) > 72;
delete from tbl_recent_co2 where hour(timediff(utc_timeStamp(),fld_time)) > 72;
delete from tbl_recent_pressure where hour(timediff(utc_timeStamp(),fld_time)) > 72;
end!!
DELIMITER ;

DELIMITER !!
create event if not exists ev_clean_historic
on schedule every 1 day
on completion preserve
do
begin
delete from tbl_historic_temperature where datediff(utc_timeStamp(),fld_start) > 365;
delete from tbl_historic_humidity where datediff(utc_timeStamp(),fld_start) > 365;
delete from tbl_historic_co2 where datediff(utc_timeStamp(),fld_start) > 365;
delete from tbl_historic_pressure where datediff(utc_timeStamp(),fld_start) > 365;
end!!
DELIMITER ;

DELIMITER !!
create procedure if not exists sp_save_historic_temperature()
begin
	# Init variables
	declare latest_historic timestamp default 0;
	declare average decimal(5,2) default null;
	declare start_time timestamp default latest_historic; 
	declare end_time timestamp default utc_timeStamp();
	
	# Fetch data for variables
	select coalesce(Max(fld_end_time),timestamp("2000-00-00", "00:00:00")) into latest_historic from tbl_historic_temperature;
	select Avg(fld_value),min(fld_time),max(fld_time) into average, start_time, end_time from tbl_recent_temperature where fld_time > latest_historic;

	# Test if viable and insert
	case 
		when average is not null then insert into tbl_historic_temperature(fld_average,fld_start_time,fld_end_time) values (average,start_time,end_time); 
		else begin end;
	end case;
end!!
DELIMITER ;

DELIMITER !!
create procedure if not exists sp_save_historic_humidity()
begin
	# Init variables
	declare latest_historic timestamp default 0;
	declare average decimal(5,2) default null;
	declare start_time timestamp default latest_historic; 
	declare end_time timestamp default utc_timeStamp();
	
	# Fetch data for variables
	select coalesce(Max(fld_end_time),timestamp("2000-00-00", "00:00:00")) into latest_historic from tbl_historic_humidity;
	select Avg(fld_value),min(fld_time),max(fld_time) into average, start_time, end_time from tbl_recent_humidity where fld_time > latest_historic;

	# Test if viable and insert
	case 
		when average is not null then insert into tbl_historic_humidity(fld_average,fld_start_time,fld_end_time) values (average,start_time,end_time); 
		else begin end;
	end case;
end!!
DELIMITER ;

DELIMITER !!
create procedure if not exists sp_save_historic_co2()
begin
	# Init variables
	declare latest_historic timestamp default 0;
	declare average decimal(5,2) default null;
	declare start_time timestamp default latest_historic; 
	declare end_time timestamp default utc_timeStamp();
	
	# Fetch data for variables
	select coalesce(Max(fld_end_time),timestamp("2000-00-00", "00:00:00")) into latest_historic from tbl_historic_co2;
	select Avg(fld_value),min(fld_time),max(fld_time) into average, start_time, end_time from tbl_recent_co2 where fld_time > latest_historic;

	# Test if viable and insert
	case 
		when average is not null then insert into tbl_historic_co2(fld_average,fld_start_time,fld_end_time) values (average,start_time,end_time); 
		else begin end;
	end case;
end!!
DELIMITER ;

DELIMITER !!
create procedure if not exists sp_save_historic_pressure()
begin
	# Init variables
	declare latest_historic timestamp default 0;
	declare average decimal(5,2) default null;
	declare start_time timestamp default latest_historic; 
	declare end_time timestamp default utc_timeStamp();
	
	# Fetch data for variables
	select coalesce(Max(fld_end_time),timestamp("2000-00-00", "00:00:00")) into latest_historic from tbl_historic_pressure;
	select Avg(fld_value),min(fld_time),max(fld_time) into average, start_time, end_time from tbl_recent_pressure where fld_time > latest_historic;

	# Test if viable and insert
	case 
		when average is not null then insert into tbl_historic_pressure(fld_average,fld_start_time,fld_end_time) values (average,start_time,end_time); 
		else begin end;
	end case;
end!!
DELIMITER ;

DELIMITER !!
create procedure if not exists sp_generate_million_data(in million int)
begin
declare i int default 0;
while i < million do
	select concat("Generating million: ",i+1,"/",million) as "Iteration";
	select "Generating million rows in tbl_recent_humidity" as "Status";
	call generate_million_humidity();
	select "Generating million rows in tbl_recent_temperature" as "Status";
	call generate_million_temperature();
	select "Generating million rows in tbl_recent_temperature" as "Status";
	call generate_million_co2();
	select "Generating million rows in tbl_recent_co2" as "Status";
	call generate_million_pressure();
	set i = i+1;
end while;
end!!
DELIMITER ;

DELIMITER !!
create procedure if not exists sp_generate_million_humidity()
begin
insert into tbl_recent_humidity(fld_time,fld_value)
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
create procedure if not exists sp_generate_million_temperature()
begin
insert into tbl_recent_temperature(fld_time,fld_value)
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
create procedure if not exists sp_generate_million_co2()
begin
insert into tbl_recent_co2(fld_time,fld_value)
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
create procedure if not exists sp_generate_million_pressure()
begin
insert into tbl_recent_pressure(fld_time,fld_value)
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
create event if not exists ev_write_historic
on schedule every 10 minute
on completion preserve
do
begin
call sp_save_historic_temperature();
call sp_save_historic_humidity();
call sp_save_historic_co2();
call sp_save_historic_pressure();
end!!
DELIMITER ;
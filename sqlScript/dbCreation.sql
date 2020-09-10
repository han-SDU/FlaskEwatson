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

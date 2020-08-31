use db_sensor;

# Mock data for tbl_co2
insert into tbl_co2(fld_time,fld_value) values(now(),2);
insert into tbl_co2(fld_time,fld_value) values(now(),66);
insert into tbl_co2(fld_time,fld_value) values(now()-10000,212);
insert into tbl_co2(fld_time,fld_value) values(now()-20000,32);
insert into tbl_co2(fld_time,fld_value) values(now()-30000,252);

# Mock data for tbl_temperature
insert into tbl_temperature(fld_time,fld_value) values(now(),4);
insert into tbl_temperature(fld_time,fld_value) values(now(),66.72);
insert into tbl_temperature(fld_time,fld_value) values(now()-10000,12.21);
insert into tbl_temperature(fld_time,fld_value) values(now()-20000,32.4);
insert into tbl_temperature(fld_time,fld_value) values(now()-30000,22.06);

# Mock data for tbl_pressure
insert into tbl_pressure(fld_time,fld_value) values(now(),3);
insert into tbl_pressure(fld_time,fld_value) values(now(),6.4);
insert into tbl_pressure(fld_time,fld_value) values(now()-10000,2.1);
insert into tbl_pressure(fld_time,fld_value) values(now()-20000,3.2);
insert into tbl_pressure(fld_time,fld_value) values(now()-30000,25.2);

# Mock data for tbl_humidity
insert into tbl_humidity(fld_time,fld_value) values(now(),5);
insert into tbl_humidity(fld_time,fld_value) values(now(),6.62);
insert into tbl_humidity(fld_time,fld_value) values(now()-10000,2.21);
insert into tbl_humidity(fld_time,fld_value) values(now()-20000,3.72);
insert into tbl_humidity(fld_time,fld_value) values(now()-30000,22.12);


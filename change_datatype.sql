alter table stock_info 
alter column open type numeric
using open::numeric;

alter table stock_info 
alter column high type numeric
using high::numeric;

alter table stock_info 
alter column low type numeric
using low::numeric;

alter table stock_info 
alter column close type numeric
using close::numeric;

alter table stock_info 
alter column volume type numeric
using volume::numeric;
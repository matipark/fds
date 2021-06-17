
-- variables required
-- manager name, table name, as_of_date

use sdfdemo_scratch

--DROP TABLE sdfdemo_scratch.dbo.ff_agg

CREATE TABLE sdfdemo_scratch.dbo.ff_agg(manager varchar(20), factset_entity_id char(8) not null, entity_proper_name varchar(200) not null, style varchar(200) null, sector varchar(200) not null, as_of_date date not null, position float null, changes_made float null, primary key (factset_entity_id, sector, as_of_date)) -- creating table

insert into sdfdemo_scratch.dbo.ff_agg -- insert into table

-- need to change the name of the fund and name of the source table

select * from ( 

SELECT 'fidelity' as manager, [factset_entity_id], [entity_proper_name], style, [l1_name], as_of_date, sum(position) as position, ISNULL(((sum(position)*1./ NULLIF(lag(sum(position), 1) OVER (PARTITION BY entity_proper_name ORDER BY as_of_date asc),0))- 1) * 100, 100) as changes_made

FROM [sdfdemo_scratch].[dbo].[ff_fidelity]

group by [factset_entity_id], [entity_proper_name], style, [l1_name], as_of_date) a

where a.as_of_date <> '2007-12-01' -- excluding the first date as it will be NULL



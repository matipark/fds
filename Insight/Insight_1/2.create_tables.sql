use sdfdemo_scratch

CREATE TABLE sdfdemo_scratch.dbo.ff_style(manager varchar(20), factset_entity_id char(8) not null, entity_proper_name varchar(200) not null, style varchar(200) null, as_of_date date not null, position float null, changes_made float null, primary key (factset_entity_id, as_of_date)) -- creating table


insert into sdfdemo_scratch.dbo.ff_style -- insert into table

-- need to change the name of the fund and name of the source table

select * from ( 

SELECT 'vanguard' as manager, [factset_entity_id], [entity_proper_name], [style], as_of_date, sum(position) as position, ISNULL(((sum(position)*1./ NULLIF(lag(sum(position), 1) OVER (PARTITION BY entity_proper_name ORDER BY as_of_date asc),0))- 1) * 100, 100) as changes_made

FROM [sdfdemo_scratch].[dbo].[ff_vanguard]

group by [factset_entity_id], [entity_proper_name], [style], as_of_date) a

where a.as_of_date <> '2019-01-01' -- excluding the first date as it will be NULL
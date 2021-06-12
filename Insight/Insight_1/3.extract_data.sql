
DECLARE @manager AS NVARCHAR(20)= '{manager}'

select case when style in ('Growth','Aggressive Growth') then 'Growth' when style in ('Value','Deep Value') then 'Value' else style end as style_agg, as_of_date, sum(case when changes_made > 0 then 1 else 0 end) as pos_chg, sum(case when changes_made < 0 then 1 else 0 end) as neg_chg, sum(case when changes_made > 0 then 1 else 0 end)-sum(case when changes_made < 0 then 1 else 0 end) as net_chg
from [sdfdemo_scratch].[dbo].[ff_style]
where manager = @manager
group by case when style in ('Growth','Aggressive Growth') then 'Growth' when style in ('Value','Deep Value') then 'Value' else style end, as_of_date
order by as_of_date, style_agg

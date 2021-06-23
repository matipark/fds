
-- aggregate value/deep value and growth/aggresive growth
-- pos_chg/neg_chg are funds that changed their position 
-- total_changed is total number of funds that changed position
-- total is the total number of funds, including those without changes
-- pct_changed is the percentage of funds that changed position
-- net_chg is pos_chg - neg_chg



DECLARE @manager AS NVARCHAR(20)= '{manager}'

select case when style in ('Growth','Aggressive Growth') then 'Growth' when style in ('Value','Deep Value') then 'Value' else style end as style_agg, as_of_date, sum(case when changes_made > 0 then 1 else 0 end) as pos_chg, sum(case when changes_made > 0 then 1 else 0 end)*1./count(changes_made) as pos_pct, sum(case when changes_made < 0 then 1 else 0 end) as neg_chg, sum(case when changes_made < 0 then 1 else 0 end)*1./count(changes_made) as neg_pct, sum(case when changes_made <> 0 then 1 else 0 end) as total_changed, count(changes_made) as total, (sum(case when changes_made <> 0 then 1 else 0 end)*1. / count(changes_made)) * 100 as pct_changed, sum(case when changes_made > 0 then 1 else 0 end)-sum(case when changes_made < 0 then 1 else 0 end) as net_chg
from [sdfdemo_scratch].[dbo].[ff_style_long]
where manager = @manager
group by case when style in ('Growth','Aggressive Growth') then 'Growth' when style in ('Value','Deep Value') then 'Value' else style end, as_of_date
order by as_of_date, style_agg

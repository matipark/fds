--Historical Fund holdings bASed on Ticker and Start Date
DECLARE @fund_ticker AS NCHAR(8)= '{fund}'; --Fund Ticker + Region, SPY-US
DECLARE @sd DATE= '{sd}'; --Earliest date for holdings
DECLARE @ed DATE= '{ed}'; --Latest date for holdings;

select *

from (


SELECT [factset_entity_id], [entity_proper_name], [style], as_of_date, sum(position) as position, ((sum(position)*1. / lag(sum(position), 1) OVER (PARTITION BY entity_proper_name ORDER BY as_of_date asc)) - 1) * 100 AS changes_made


FROM [sdfdemo_scratch].[dbo].[ff_blackrock]

where as_of_date in ('2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01')
group by [factset_entity_id], [entity_proper_name], [style], as_of_date) Data


where as_of_date = '2020-04-01' and changes_made > 0


order by changes_made asc

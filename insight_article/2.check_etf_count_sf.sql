select count(*)
from "FDS"."ETF_V1"."ETF_REFERENCE"
where index_name like '%ESG%' and launch_date between '2020-01-01' and '2021-12-31'

select count(*)
from "FDS"."ETF_V1"."ETF_REFERENCE"
where index_name like '%ESG%' and launch_date between '2018-01-01' and '2019-12-31'

select count(*)
from "FDS"."ETF_V1"."ETF_REFERENCE"
where index_name like '%ESG%' and launch_date between '2016-01-01' and '2017-12-31'

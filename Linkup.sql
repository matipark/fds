

-- FUll table

SELECT TOP 100 *
  FROM sdfdemodx.lu_v1.lu_ticker_analytics an
  join sym_v1.sym_ticker_region reg on an.lu_ticker_region = reg.ticker_region
  join sym_v1.sym_coverage sym on reg.fsym_id = sym.fsym_id --fsym_id is regional
  join fp_v2.fp_basic_prices prices on sym.fsym_id = prices.fsym_id and an.lu_date = prices.p_date
  join fp_v2.fp_total_returns_daily retr on sym.fsym_id = retr.fsym_id and an.lu_date = retr.p_date
  join sym_v1.sym_sec_entity en on sym.fsym_primary_equity_id = en.fsym_id
  join rbics_v1.rbics_entity_focus rb on rb.factset_entity_id = en.factset_entity_id
  join rbics_v1.rbics_structure st on rb.l6_id = st.l6_id
  where fref_listing_exchange = 'HKG' and rb.end_date is null and st.end_date is null -- and st.l2_name = 'banking'
  order by lu_date desc


-- avg_job

SELECT an.lu_date as date, st.l2_name as industry, sum(an.lu_unique_active_job_count)/count(an.lu_unique_active_job_count) as avg_job
  FROM sdfdemodx.lu_v1.lu_ticker_analytics an
  join sym_v1.sym_ticker_region reg on an.lu_ticker_region = reg.ticker_region
  join sym_v1.sym_coverage sym on reg.fsym_id = sym.fsym_id --fsym_id is regional
  --join fp_v2.fp_basic_prices prices on sym.fsym_id = prices.fsym_id and an.lu_date = prices.p_date
  join fp_v2.fp_total_returns_daily retr on sym.fsym_id = retr.fsym_id and an.lu_date = retr.p_date
  join sym_v1.sym_sec_entity en on sym.fsym_primary_equity_id = en.fsym_id
  join rbics_v1.rbics_entity_focus rb on rb.factset_entity_id = en.factset_entity_id
  join rbics_v1.rbics_structure st on rb.l6_id = st.l6_id
  where fref_listing_exchange = 'HKG' and rb.end_date is null and st.end_date is null -- and an.lu_ticker_region = '1-HK'
  group by an.lu_date, st.l2_name
  order by st.l2_name, an.lu_date desc



-- proof daily return calc

SELECT 

an.lu_date as date, st.l2_name as industry, sum(an.lu_unique_active_job_count) as job_count, count(an.lu_unique_active_job_count) as companies_count, (case when sum(an.lu_unique_active_job_count)/count(an.lu_unique_active_job_count) = 0 then null else sum(an.lu_unique_active_job_count)/count(an.lu_unique_active_job_count) end) as avg_job

, (exp(sum(log(1+(one_day_pct/100))))-1)*100 as daily_price_return
--,log(1+(one_day_pct/100))
,sum(log(1+(one_day_pct/100)))
,sum(1+(one_day_pct/100))
,avg(one_day_pct)


  FROM sdfdemodx.lu_v1.lu_ticker_analytics an
  join sym_v1.sym_ticker_region reg on an.lu_ticker_region = reg.ticker_region
  join sym_v1.sym_coverage sym on reg.fsym_id = sym.fsym_id --fsym_id is regional
  --join fp_v2.fp_basic_prices prices on sym.fsym_id = prices.fsym_id and an.lu_date = prices.p_date
  join fp_v2.fp_total_returns_daily retr on sym.fsym_id = retr.fsym_id and an.lu_date = retr.p_date
  join sym_v1.sym_sec_entity en on sym.fsym_primary_equity_id = en.fsym_id
  join rbics_v1.rbics_entity_focus rb on rb.factset_entity_id = en.factset_entity_id
  join rbics_v1.rbics_structure st on rb.l6_id = st.l6_id
  where fref_listing_exchange = 'HKG' and rb.end_date is null and st.end_date is null
  group by an.lu_date, st.l2_name



-- Latest

SELECT industry, date, job_count, companies_count, avg_job, 

((avg_job*1. / lag(avg_job, 1) OVER (PARTITION BY industry ORDER BY date asc)) - 1) * 100 AS daily_return -- calculating daily job count return by sector
, daily_price_return

FROM 

(SELECT an.lu_date as date, st.l2_name as industry, sum(an.lu_unique_active_job_count) as job_count, count(an.lu_unique_active_job_count) as companies_count, (case when avg(an.lu_unique_active_job_count) = 0 then null else avg(an.lu_unique_active_job_count) end) as avg_job, avg(one_day_pct) as daily_price_return -- arithmetic daily return by sector

  FROM sdfdemodx.lu_v1.lu_ticker_analytics an
  join sym_v1.sym_ticker_region reg on an.lu_ticker_region = reg.ticker_region
  join sym_v1.sym_coverage sym on reg.fsym_id = sym.fsym_id --fsym_id is regional
  join fp_v2.fp_total_returns_daily retr on sym.fsym_id = retr.fsym_id and an.lu_date = retr.p_date -- daily total returns
  join sym_v1.sym_sec_entity en on sym.fsym_primary_equity_id = en.fsym_id -- linking it to entity ID
  join rbics_v1.rbics_entity_focus rb on rb.factset_entity_id = en.factset_entity_id -- pull rbics L6
  join rbics_v1.rbics_structure st on rb.l6_id = st.l6_id -- pull rest of rbics
  where fref_listing_exchange = 'NYS' and rb.end_date is null and st.end_date is null
  group by an.lu_date, st.l2_name) a
  order by industry, date desc






/*

[lu_v1].[lu_jobs] list of individual jobs 
[lu_v1].[lu_company_analytics] list of jobs by company by date
[lu_v1].[lu_factset_id_map]
[lu_v1].[lu_ticker_analytics] ticker, ticker exchange




(exp(sum(log(1+(one_day_pct/100))))-1)*100 -- time-series return

*/
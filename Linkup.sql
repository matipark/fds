

SELECT TOP 100 *
  FROM sdfdemodx.lu_v1.lu_ticker_analytics an
  join sym_v1.sym_ticker_region reg on an.lu_ticker_region = reg.ticker_region
  join sym_v1.sym_coverage sym on reg.fsym_id = sym.fsym_id --fsym_id is regional
  --join fp_v2.fp_basic_prices prices on sym.fsym_id = prices.fsym_id and an.lu_date = prices.p_date
  join fp_v2.fp_total_returns_daily retr on sym.fsym_id = retr.fsym_id and an.lu_date = retr.p_date
  join sym_v1.sym_sec_entity en on sym.fsym_primary_equity_id = en.fsym_id
  join rbics_v1.rbics_entity_focus rb on rb.factset_entity_id = en.factset_entity_id
  join rbics_v1.rbics_structure st on rb.l6_id = st.l6_id
  where fref_listing_exchange = 'HKG' and rb.end_date is null and st.end_date is null and an.lu_ticker_region = '1-HK'
  order by lu_date desc




SELECT an.lu_date as date, st.l2_name as industry, sum(an.lu_unique_active_job_count)/count(an.lu_unique_active_job_count) as avg_job
  FROM sdfdemodx.lu_v1.lu_ticker_analytics an
  join sym_v1.sym_ticker_region reg on an.lu_ticker_region = reg.ticker_region
  join sym_v1.sym_coverage sym on reg.fsym_id = sym.fsym_id --fsym_id is regional
  --join fp_v2.fp_basic_prices prices on sym.fsym_id = prices.fsym_id and an.lu_date = prices.p_date
  join fp_v2.fp_total_returns_daily retr on sym.fsym_id = retr.fsym_id and an.lu_date = retr.p_date
  join sym_v1.sym_sec_entity en on sym.fsym_primary_equity_id = en.fsym_id
  join rbics_v1.rbics_entity_focus rb on rb.factset_entity_id = en.factset_entity_id
  join rbics_v1.rbics_structure st on rb.l6_id = st.l6_id
  where fref_listing_exchange = 'HKG' and rb.end_date is null and st.end_date is null-- and an.lu_ticker_region = '1-HK'
  group by an.lu_date, st.l2_name
  order by an.lu_date desc


/*

[lu_v1].[lu_jobs] list of individual jobs 
[lu_v1].[lu_company_analytics] list of jobs by company by date
[lu_v1].[lu_factset_id_map]
[lu_v1].[lu_ticker_analytics] ticker, ticker exchange

*/
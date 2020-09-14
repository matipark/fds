


use sdfdemo
declare @hldrid varchar(20)
declare @pricedate date
declare @histdate date
declare @daysback integer
declare @daysahead integer
set @hldrid = '000KLZ-E'
set @histdate = '2020-06-30'
--as of date
set @daysback = -730
--number of days prior to the @histdate that the holdings would be considered valid
set @daysahead = 0
--number of days after the @histdate that the holdings would be condidered valid
set @pricedate = (select max(price_date) from own_v5.own_sec_prices
where price_date between dateadd(dd,@daysback,@histdate) and dateadd(dd,@daysahead,@histdate))


insert into sdfdemo_scratch.dbo.KLZE
	(fsym_id, factset_entity_id, security_name, exchange, country_desc, l1_name, l2_name, l3_name, l4_name, position, mkt_val, report_date, as_of_date, source)


select best_fit.fsym_id
, en.factset_entity_id
, co.proper_name security_name
, coe.fref_listing_exchange exchange
, cou.country_desc
, st.l1_name
, st.l2_name
, st.l3_name
, st.l4_name
, holding position
, holding * p.adj_price mkt_val
, report_date
, @histdate as_of_date
, source
from
	(
	select own_master.fsym_id

--Holding

	, case
		when own_master.fds_uksr_flag = 1 and own_master.stk_source in ('W','O')
		then
			case
				when own_master.stk_report_date > dateadd(mm,-18,@histdate)
				then own_master.stk_holding
				else own_master.sof_holding
			end
		when own_master.inst_13f_flag = 1 and own_master.sec_13f_flag = 1
		then 
			case 
				when own_master.stk_report_date > own_master.tf_report_date
				then own_master.stk_holding
				else own_master.tf_holding
			end
		when own_master.inst_13f_flag = 1 and own_master.sec_13f_ca_flag = 1
		then
			case
				when own_master.stk_report_date > own_master.tf_report_date
				then own_master.stk_holding
				else isnull(own_master.tf_holding,isnull(own_master.stk_holding,own_master.sof_holding))
			end
		when own_master.inst_13f_flag = 0 or (own_master.sec_13f_flag = 0 and own_master.sec_13f_ca_flag = 0 )
			then isnull(own_master.stk_holding,own_master.sof_holding)
		else null
		end as holding
	
	
--Report date
	
	, case 
		when own_master.fds_uksr_flag = 1 and own_master.stk_source in ('W','O')
		then
			case
				when own_master.stk_report_date > dateadd(mm,-18,@histdate)
				then own_master.stk_report_date
				else own_master.sof_report_date
			end
		when own_master.inst_13f_flag = 1 and own_master.sec_13f_flag = 1
		then 
			case 
				when own_master.stk_report_date > own_master.tf_report_date
				then own_master.stk_report_date
				else own_master.tf_report_date
			end
		when own_master.inst_13f_flag = 1 and own_master.sec_13f_ca_flag = 1
		then
			case
				when own_master.stk_report_date > own_master.tf_report_date
				then own_master.stk_report_date
				else isnull(own_master.tf_report_date,isnull(own_master.stk_report_date,own_master.sof_report_date))
			end
		when own_master.inst_13f_flag = 0 or (own_master.sec_13f_flag = 0 and own_master.sec_13f_ca_flag = 0 )
			then isnull(own_master.stk_report_date,own_master.sof_report_date)
		else null
		end as report_date


--Source

	, case 
		when own_master.inst_13f_flag = 1 and own_master.sec_13f_flag = 1
		then 
			case 
				when own_master.stk_report_date > own_master.tf_report_date
				then (select source_desc
		from ref_v2.source_map
		where source_code = own_master.stk_source)
				else '13F Form'
			end
		when own_master.inst_13f_flag = 1 and own_master.sec_13f_ca_flag = 1
		then
			case
				when own_master.stk_report_date > own_master.tf_report_date
				then (select source_desc
		from ref_v2.source_map
		where source_code = own_master.stk_source)
				else 
					case
						when own_master.tf_holding is not null
						then '13F Form'
						when own_master.stk_holding is not null
						then (select source_desc
		from ref_v2.source_map
		where source_code = own_master.stk_source)
						else 'Sum of Funds'
					end
			end
		when (own_master.inst_13f_flag = 0 or (own_master.sec_13f_flag = 0 and own_master.sec_13f_ca_flag =0 )) and own_master.stk_holding is not null
		then (select source_desc
		from ref_v2.source_map
		where source_code = own_master.stk_source)
		when (own_master.inst_13f_flag = 0 or (own_master.sec_13f_flag = 0 and own_master.sec_13f_ca_flag =0 )) and own_master.stk_holding is null
			then 'Sum of Funds'
		else null
		end as source





	from
		(
			select co.fsym_id
			, all_sources.*
			, i.fds_13f_flag inst_13f_flag
			, oc.fds_13f_flag sec_13f_flag
			, oc.fds_13f_ca_flag sec_13f_ca_flag
			, oc.fds_uksr_flag
		from sym_v1.sym_coverage co
			join
			(
				select *
			from
				(
					--query for 13f positions at rollup_entity level
					select h.fsym_id tf_fsym_id
					, max(h.report_date) tf_report_date
					, sum(h.adj_holding) tf_holding
				from own_v5.own_inst_13f_detail h
					join own_v5.own_ent_13f_combined_inst ci on ci.factset_filer_entity_id = h.factset_entity_id
					join --select the latest report date for 13f filers within the window
					(
						select max(fh.report_date) as max_date
						, ci.factset_rollup_entity_id
					from own_v5.own_ent_13f_filing_hist fh
						join own_v5.own_ent_13f_combined_inst ci on ci.factset_filer_entity_id = fh.factset_13f_filer_entity_id
					where fh.report_date between dateadd(dd,@daysback,@histdate) and dateadd(dd,@daysahead,@histdate)
					group by ci.factset_rollup_entity_id
					) md on md.max_date = h.report_date and md.factset_rollup_entity_id = ci.factset_rollup_entity_id
				where ci.factset_rollup_entity_id = @hldrid
				group by h.fsym_id
				) tf


				full outer join


				(
					--query for institutional stakeholder positions
					select h.fsym_id stk_fsym_id
					, h.as_of_date stk_report_date
					, h.position stk_holding
					, h.source_code stk_source
				from own_v5.own_inst_stakes_detail h
					--join on subquery that finds most recent report_date within the window
					join (
						   select max(d.as_of_date) max_report_date
						   , d.factset_entity_id
						   , d.fsym_id
					from own_v5.own_inst_stakes_detail d
					where d.as_of_date BETWEEN DATEADD(DD,@DAYSBACK,@HISTDATE) AND DATEADD(DD,@DAYSAHEAD,@HISTDATE)
					group by d.factset_entity_id, d.fsym_id
					) md on md.factset_entity_id = h.factset_entity_id and md.fsym_id = h.fsym_id and md.max_report_date = h.as_of_date
				where h.factset_entity_id = @hldrid
				) stk on stk.stk_fsym_id = tf.tf_fsym_id


				full outer join


				(
					--query for sum of funds positions
					select h.fsym_id sof_fsym_id
					, sum(h.adj_holding) sof_holding
					, max(h.report_date) sof_report_date
				from own_v5.own_fund_detail h
					join own_v5.own_ent_funds f on f.factset_fund_id = h.factset_fund_id and f.active_flag = 1
					join
					(
						select max(fh.report_date) as max_date, fh.factset_fund_id
					from own_v5.own_ent_fund_filing_hist fh
					where fh.report_date between dateadd(dd,@daysback,@histdate) and dateadd(dd,@daysahead,@histdate)
					group by fh.factset_fund_id
					) md on md.max_date = h.report_date and md.factset_fund_id = h.factset_fund_id
				where f.factset_inst_entity_id = @hldrid
				group by h.fsym_id
				) sof on sof.sof_fsym_id = tf.tf_fsym_id or sof.sof_fsym_id = stk.stk_fsym_id



			) all_sources on all_sources.tf_fsym_id = co.fsym_id or all_sources.stk_fsym_id = co.fsym_id or all_sources.sof_fsym_id = co.fsym_id
			left join own_v5.own_ent_institutions i on i.factset_entity_id = @hldrid
			left join own_v5.own_sec_coverage oc on oc.fsym_id = co.fsym_id
		where oc.universe_type = 'EQ' and oc.issue_type != 'OE'
	) own_master
		left join own_v5.own_sec_coverage oc on oc.fsym_id = own_master.fsym_id
) best_fit



	join sym_v1.sym_coverage co on co.fsym_id = best_fit.fsym_id
	join sym_v1.sym_coverage coe on coe.fsym_id = co.fsym_primary_listing_id
	join sym_v1.sym_sec_entity en on co.fsym_id = en.fsym_id
	join sym_v1.sym_entity en2 on en.factset_entity_id = en2.factset_entity_id
	join ref_v2.country_map cou on cou.iso_country = en2.iso_country
	join rbics_v1.rbics_entity_focus rb on rb.factset_entity_id = en.factset_entity_id
	join rbics_v1.rbics_structure st on rb.l6_id = st.l6_id
	join own_v5.own_sec_prices p on p.fsym_id = best_fit.fsym_id and p.price_date = @pricedate
where best_fit.holding is not null and rb.end_date is null and st.end_date is null
order by mkt_val desc


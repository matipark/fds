use sdfdemo
declare @hldrid varchar(20)
declare @pricedate date
declare @histdate date
declare @daysback integer
declare @daysahead integer
set @hldrid = '000KLZ-E'
set @histdate = '2019-07-01'
--as of date
set @daysback = -730
--number of days prior to the @histdate that the holdings would be considered valid
set @daysahead = 0
--number of days after the @histdate that the holdings would be condidered valid
set @pricedate = (select max(price_date) from own_v5.own_sec_prices
where price_date between dateadd(dd,@daysback,@histdate) and dateadd(dd,@daysahead,@histdate))



--CREATE TABLE sdfdemo_scratch.dbo.TAB_FIDEL_FF(factset_entity_id char(8) not null, entity_proper_name varchar(200) not null, fsym_id char(8) not null, proper_name varchar(200) not null, exchange varchar(40) null, country_desc varchar(24) null, l1_name varchar(200) null, l2_name varchar(200) null, l3_name varchar(200) null, l4_name varchar(200) null, position float null, mkt_val float null, report_date date null, as_of_date date not null, primary key (factset_entity_id, fsym_id, as_of_date))

--drop TABLE sdfdemo_scratch.dbo.TAB_FIDEL_FF

insert into sdfdemo_scratch.dbo.TAB_FIDEL_FF

select --top 100

ent.factset_entity_id
, ent.entity_proper_name
, h.fsym_id
, sym.proper_name
, coe.fref_listing_exchange exchange
, cou.country_desc
, st.l1_name
, st.l2_name
, st.l3_name
, st.l4_name
, h.adj_holding position
, h.adj_holding * p.adj_price mkt_val
, h.report_date
, @histdate as_of_date
from own_v5.own_fund_detail h
join own_v5.own_ent_funds f on f.factset_fund_id = h.factset_fund_id and f.active_flag = 1

join

(
select max(fh.report_date) as max_date, fh.factset_fund_id
from own_v5.own_ent_fund_filing_hist fh
where fh.report_date between dateadd(dd,@daysback,@histdate) and dateadd(dd,@daysahead,@histdate)
group by fh.factset_fund_id
) md on md.max_date = h.report_date and md.factset_fund_id = h.factset_fund_id


join sym_v1.sym_entity ent on f.Factset_Fund_ID = ent.[factset_entity_id]
join sym_v1.sym_coverage sym on sym.fsym_id = h.fsym_id
join sym_v1.sym_coverage coe on coe.fsym_id = sym.fsym_primary_listing_id
join sym_v1.sym_sec_entity en on sym.fsym_id = en.fsym_id
join sym_v1.sym_entity en2 on en.factset_entity_id = en2.factset_entity_id
join ref_v2.country_map cou on cou.iso_country = en2.iso_country
join rbics_v1.rbics_entity_focus rb on rb.factset_entity_id = en.factset_entity_id
join rbics_v1.rbics_structure st on rb.l6_id = st.l6_id
join own_v5.own_sec_prices p on p.fsym_id = h.fsym_id and p.price_date = @pricedate

where f.factset_inst_entity_id = @hldrid
and h.adj_holding is not null and rb.end_date is null and st.end_date is null

--Historical Fund holdings bASed on Ticker and Start Date
DECLARE @fund_ticker AS NCHAR(8)= '{fund}'; --Fund Ticker + Region, SPY-US
DECLARE @sd DATE= '{sd}'; --Earliest date for holdings
DECLARE @ed DATE= '{ed}'; --Latest date for holdings;
WITH hist
     AS (SELECT DISTINCT 
                fi.factset_fund_id, 
                fh.report_date, 
                DATEDIFF(DAY, LAG(report_date, 1, report_date) OVER(PARTITION BY fi.factset_fund_id
                ORDER BY report_date), fh.report_date) AS rpt_gap
         FROM   sym_v1.sym_ticker_region AS tr
         JOIN sym_v1.sym_coverage AS cov
           ON tr.fsym_id = cov.fsym_id
         JOIN own_v5.own_ent_fund_identifiers AS fi
           ON fi.fund_identifier = cov.fsym_security_id
         JOIN own_v5.own_ent_fund_filing_hist AS fh
           ON fh.factset_fund_id = fi.factset_fund_id
         WHERE  tr.ticker_region = @fund_ticker
                AND fh.report_date BETWEEN @sd AND @ed),
     own
     AS (SELECT fd.factset_fund_id, 
                se.factset_entity_id, 
                fd.report_date, 
                h.rpt_gap
         FROM   hist AS h
         JOIN own_v5.own_fund_detail AS fd
           ON h.factset_fund_id = fd.factset_fund_id
              AND h.report_date = fd.report_date
         JOIN own_v5.own_sec_entity_hist AS se
           ON se.fsym_id = fd.fsym_id
              AND se.start_date <= fd.report_date
              AND (se.end_date > fd.report_date
                   OR se.end_date IS NULL)),
     gaps
     AS (SELECT *,
                CASE
                    WHEN DATEDIFF(DAY, LAG(report_date) OVER(PARTITION BY factset_entity_id
                         ORDER BY report_date), report_date) <= rpt_gap
                    THEN 0
                    ELSE 1
                END AS isstart
         FROM   own),
     grp
     AS (SELECT *, 
                SUM(isstart) OVER(PARTITION BY factset_entity_id
                ORDER BY report_date ROWS UNBOUNDED PRECEDING) AS grp
         FROM   gaps),
     univ
     AS (SELECT factset_entity_id, 
                MIN(report_date) AS startdate, 
                MAX(report_date) AS enddate
         FROM   grp
         GROUP BY factset_entity_id, 
                  grp)
     SELECT factset_entity_id, 
            startdate, 
            enddate
     FROM   univ;
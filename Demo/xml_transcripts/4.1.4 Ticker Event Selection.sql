DECLARE @start_date AS DATE = '{start_date}'; --'2019-04-01'
DECLARE @end_date AS DATETIME = '{end_date}' ;--'2020-04-01'
DECLARE @ticker AS NVARCHAR(MAX) = '{ticker}' ;--'MSFT-US'
DECLARE @call_type AS NVARCHAR(MAX) = '{call_type}'; --'Earnings Call'

SELECT tr.ticker_region,
       t.actr_tr_id,
       t.actr_call_time, 
       t.actr_call_type, 
       t.actr_section, 
       t.actr_name, 
       t.actr_title, 
       t.actr_affiliation, 
       tm.actr_topic_desc,
       t.actr_topic,
       t.actr_topic_count,
       t.actr_word_count,
       t.actr_sentiment, 
       t.actr_confidence, 
       t.actr_prob_pos, 
       t.actr_prob_ntr, 
       t.actr_prob_neg
FROM   sym_v1.sym_ticker_region AS tr
JOIN sym_v1.sym_coverage AS cov
  ON tr.fsym_id = cov.fsym_id
JOIN actr_v1.actr_factset_id_map AS id
  ON id.factset_id = cov.fsym_security_id
JOIN actr_v1.actr_transcripts AS t
  ON t.actr_company_id = id.provider_id
--Ensure only most up-to-date transcript versions are used
JOIN
(
    SELECT maxt.actr_tr_id, 
           maxt.actr_company_id, 
           MAX(maxt.actr_version_id) AS max_version
    FROM   actr_v1.actr_transcripts AS maxt
    WHERE maxt.actr_call_time BETWEEN @start_date AND @end_date
       AND maxt.actr_call_type = @call_type
    GROUP BY actr_tr_id, 
             actr_company_id
) AS latest_tr
  ON t.actr_version_id = latest_tr.max_version
JOIN actr_v1.actr_topic_map AS tm 
  ON tm.actr_topic = t.actr_topic
WHERE  tr.ticker_region = @ticker
       AND (t.actr_call_time BETWEEN @start_date AND @end_date)
       AND actr_call_type = @call_type
ORDER BY actr_call_time DESC;
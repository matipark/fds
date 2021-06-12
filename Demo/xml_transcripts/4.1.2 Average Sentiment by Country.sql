DECLARE @start_date AS DATE= '{start_date}'; --'2020-01-01' 
DECLARE @end_date AS DATE= '{end_date}';  --'2020-04-01'

SELECT icm.actr_country_name, 
       COUNT(DISTINCT atr.actr_tr_id) AS count_transcript_id
FROM   actr_v1.actr_transcripts AS atr
JOIN actr_v1.actr_iso_country_map AS icm
  ON icm.actr_iso_country_3 = atr.actr_iso_country_3
WHERE  atr.actr_call_time BETWEEN @start_date AND @end_date
GROUP BY icm.actr_country_name
ORDER BY count_transcript_id DESC;
SELECT atr.actr_call_type, 
       COUNT(DISTINCT atr.actr_tr_id) AS transcript_count
FROM   actr_v1.actr_transcripts AS atr
GROUP BY atr.actr_call_type
ORDER BY transcript_count desc;
DECLARE @sd DATE= '{sd}'; --Earliest date for holdings
DECLARE @ed DATE= '{ed}'; --Latest date for holdings
SELECT tr.ticker_region, 
       se.factset_entity_id, 
       ent.entity_proper_name, 
       ce.event_datetime_utc, 
       tm.event_type_display_name, 
       tv.transcript_type,
       cr.report_id, 
       ce.title, 
       CAST(YEAR(event_datetime_utc) AS VARCHAR) AS directory, 
       replace(CAST(CAST(ce.event_datetime_utc AS DATE) AS VARCHAR), '-', '') + '-' + CAST(cr.report_id AS VARCHAR) + '-' + tv.transcript_type + '.xml' AS xml_filename
FROM   sym_v1.sym_ticker_region AS tr
JOIN sym_v1.sym_coverage AS cov
  ON cov.fsym_primary_listing_id = tr.fsym_id
     AND cov.fsym_id = cov.fsym_primary_equity_id
JOIN evt_v1.ce_sec_entity_hist AS se
  ON se.fsym_id = cov.fsym_security_id
JOIN sym_v1.sym_entity AS ent
  ON ent.factset_entity_id = se.factset_entity_id
JOIN evt_v1.ce_reports AS cr
  ON cr.factset_entity_id = ent.factset_entity_id
JOIN evt_v1.ce_events AS ce
  ON ce.event_id = cr.event_id
     AND se.start_date <= ce.event_datetime_utc
     AND (se.end_date > ce.event_datetime_utc
          OR se.end_date IS NULL)
JOIN ref_v2.ce_event_type_map AS tm
  ON tm.event_type_code = ce.event_type
JOIN
(
    SELECT tv.report_id, 
           tv.transcript_type, 
           MAX(tv.version_id) AS version_id, 
           MAX(tv.upload_datetime) AS upload_datetime
    FROM   evt_v1.ce_transcript_versions AS tv
    GROUP BY tv.report_id, 
             tv.transcript_type
) AS tv
  ON tv.report_id = cr.report_id
WHERE  cr.factset_entity_id IN({entity_ids})
       AND ce.event_datetime_utc >= @sd
       AND ce.event_datetime_utc <= @ed
ORDER BY ce.event_datetime_utc DESC, 
         tv.upload_datetime DESC;
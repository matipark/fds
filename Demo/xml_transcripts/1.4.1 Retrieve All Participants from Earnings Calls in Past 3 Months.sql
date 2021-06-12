SELECT ce.event_id, 
       cr.report_id, 
       ent.factset_entity_id, 
       ent.entity_proper_name, 
       ce.event_datetime_utc, 
       ce.title, 
       cp.factset_person_id, 
       cp.participant_title, 
       ppl.entity_proper_name AS person_name, 
       ppl_ent.factset_entity_id AS person_comp_entity_id, 
       ppl_ent.entity_proper_name AS person_comp_name
FROM   evt_v1.ce_events AS ce
JOIN evt_v1.ce_reports AS cr
  ON ce.event_id = cr.event_id
JOIN sym_v1.sym_entity AS ent
  ON ent.factset_entity_id = cr.factset_entity_id
JOIN evt_v1.ce_participants AS cp
  ON cp.report_id = cr.report_id
JOIN sym_v1.sym_entity AS ppl
  ON ppl.factset_entity_id = cp.factset_person_id
JOIN sym_v1.sym_entity AS ppl_ent
  ON ppl_ent.factset_entity_id = cp.factset_entity_id
WHERE  ce.event_datetime_utc >= DATEADD(MONTH, -3, GETDATE()) --limit to events in past 3 months
       AND ce.event_type = 'E'; -- Limit to  earnings calls
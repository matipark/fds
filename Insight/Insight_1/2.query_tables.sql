use sdfdemo_scratch

SELECT 'fidelity' as manager, [factset_entity_id], [entity_proper_name], [style], as_of_date, sum(position) as position, ISNULL(((sum(position)*1./ NULLIF(lag(sum(position), 1) OVER (PARTITION BY entity_proper_name ORDER BY as_of_date asc),0))- 1) * 100, 100) as changes_made

FROM [sdfdemo_scratch].[dbo].[ff_fidelity]
where factset_entity_id = '04B8BR-E'
group by [factset_entity_id], [entity_proper_name], [style], as_of_date
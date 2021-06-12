SELECT TOP 100 b.factset_entity_id, b.entity_proper_name, c.total_aum
  FROM [own_v5].[own_ent_fund_managers] a
  join [sym_v1].[sym_entity] b on a.factset_inst_entity_id = b.factset_entity_id
  join [own_v5].[own_ent_institutions] c on b.factset_entity_id = c.factset_entity_id
  where b.entity_proper_name like '%UBS%'
  group by b.factset_entity_id, b.entity_proper_name, c.total_aum
  order by total_aum desc
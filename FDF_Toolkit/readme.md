# FDF V2 portal toolkit
### Latest version v2.4 (2022-06-04)

This toolkit will pick up the required fields from the excel file and automatically select tables/column in the filtering portal


## Compatible packages

1. Fundamentals
    - Basic
    - Advanced
2. Estimates
    - Basic
    - Advanced
3. Symbology


## How to use

Download and copy over the latest version of the toolkit to Virtual Environment together with the excel template that contains the list of the fields and queries.

Name of the excel file should not be changed.

## Fields (Excel first sheet)

First tab requires fields only - this list will be applied to all tables that have these fields available. You don't need to add the primary key for each table as they will be picked up automatically. You can leave this page empty if you don't need this functionality or you already have the fields filter setup on the portal and you want to keep it as is. Symbology table does not support filtering by fields.

## Queries (Excel second sheet)

Second tab requires bundle names in the column A and queries in the column B. You can leave this page empty if not needed.

Bundle names must follow the syntax below:

1. ff_basic - FactSet Fundamentals Basic/Advanced
2. ff_basic_cf - FactSet Fundamentals CF 
3. fe_basic_act - FactSet Estimates Basic Actuals
4. fe_basic_conh - FactSet Estimates Basic Consensus
5. fe_basic_guid - FactSet Estimates Basic Guidance
6. fe_advanced_act - FactSet Estimates Advanced Actuals
7. fe_advanced_conh - FactSet Estimates Advanced Consensus
8. fe_advanced_guid - FactSet Estimates Advanced Guidance
9. sym_hub - Symbology Hub

\* symbology only supports sym_coverage table
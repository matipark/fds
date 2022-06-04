# FDF V2 portal toolkit
### Latest release v2.4

This tool will pick up the required fields from the excel file and automatically select tables/column in the filtering portal

## Compatible packages

1. Fundamentals
    - Basic
    - Advanced
2. Estimates
    - Basic
    - Advanced
3. Symbology


## Fields (first sheet)

First tab requires fields only- this list will be applied to all tables that have these fields available. You don't need to add the primary key for each table as they will be picked up automatically. You can leave this page empty if you don't need this functionality or you already have the fields filter setup on the portal and you want to keep it as is. Symbology table does not support filtering by fields.

## Queries

Second tab requires bundle names in the column A and queries in the column B. Bundle names must follow the syntax below:

ff_basic - FactSet Fundamentals Basic/Advanced
ff_basic_cf - FactSet Fundamentals CF 
fe_basic_act - FactSet Estimates Basic Actuals
fe_basic_conh - FactSet Estimates Basic Consensus
fe_basic_guid - FactSet Estimates Basic Guidance
fe_advanced_act - FactSet Estimates Advanced Actuals
fe_advanced_conh - FactSet Estimates Advanced Consensus
fe_advanced_guid - FactSet Estimates Advanced Guidance
sym_hub - Symbology Hub

symbology only supports sym_coverage table

## Excel template

Name: fdf_custom.xlsm 

This file must be copied over to Virtual Environment together with the latest version of the toolkit

Second tab 
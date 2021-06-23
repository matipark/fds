#%%

import queries as q

username_list = ['prism_kr', 'perpetual', 'yonhap_kr','mac_cs_au','Doom_KR']
start_date = 'now-7d'
max_size = 10
apikey = 'apikey 6b9ea362-bcdf-4fcc-b0a0-d693a978a7bd' 



#%%


q.generate_excel(apikey,username_list,start_date,max_size)


#%%

# Reference
# https://www.elastic.co/guide/en/kibana/current/settings.html
# https://www.youtube.com/watch?v=mbd1YI_mzbk
# https://marcobonzanini.com/2015/02/02/how-to-query-elasticsearch-with-python/
# https://medium.com/a-layman/apm-logging-services-part-3-create-a-python-client-to-fetch-data-from-elasticsearch-532c828db784

# saving to excel
# https://xlsxwriter.readthedocs.io/working_with_pandas.html
# https://xlsxwriter.readthedocs.io/working_with_cell_notation.html#cell-notation

### FDS Reference

# https://pages.github.factset.com/clp/docs/api/native-searching-cloud/
# http://is.factset.com/rpd/summary.aspx?messageId=58289251
# https://pages.github.factset.com/clp/factset-io-addon-clp/
# https://github.factset.com/clp/python-logging-clp
# https://github.factset.com/FactSet?q=&type=&language=
# http://log.factset.io/manage/api-keys


#%%


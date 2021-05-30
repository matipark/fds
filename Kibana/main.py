#%%

import queries as q
import pandas as pd
from openpyxl import load_workbook


# %%

username = 'PERPETUAL'
start_date = 'now-30d'

# %%

content_endpoint = q.content_api_endpoint(username,start_date).json()
data = content_endpoint['aggregations']['2']['buckets']

content_result_df = pd.json_normalize(data)
content_result_df.insert(0 ,'username', username)

content_result_df

#%%

# 엑셀파일 저장 
def saving_excel(content_result_df):

    writer = pd.ExcelWriter('usage_output.xlsx', engine='openpyxl')
    # try to open an existing workbook
    writer.book = load_workbook('usage_output.xlsx')
    # copy existing sheets
    writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)

    # read existing file
    reader = pd.read_excel(r'usage_output.xlsx')
    # write out the new sheet
    content_result_df.to_excel(writer, sheet_name=username, startcol=writer.sheets['Sheet1'].max_column, index = False,header= False) #startrow=len(reader)+1)

    writer.close()

saving_excel(content_result_df)


# %%

# https://www.elastic.co/guide/en/kibana/current/settings.html
# https://www.youtube.com/watch?v=mbd1YI_mzbk
# https://marcobonzanini.com/2015/02/02/how-to-query-elasticsearch-with-python/
# https://medium.com/a-layman/apm-logging-services-part-3-create-a-python-client-to-fetch-data-from-elasticsearch-532c828db784


### FDS Reference

# https://pages.github.factset.com/clp/docs/api/native-searching-cloud/
# http://is.factset.com/rpd/summary.aspx?messageId=58289251
# https://pages.github.factset.com/clp/factset-io-addon-clp/
# https://github.factset.com/clp/python-logging-clp
# https://github.factset.com/FactSet?q=&type=&language=

#%%

import queries as q
import pandas as pd
import time 
from openpyxl import load_workbook



# %%

username = 'prism_kr' #'PERPETUAL' #'yonhap_kr' #'PERPETUAL'
start_date = 'now-30d'
#serial = 1215045 #1137568
max_size = 10
apikey = 'apikey 6b9ea362-bcdf-4fcc-b0a0-d693a978a7bd' #'apikey a8b298e2-5fc6-4fb5-a6a7-cf22267ba9ab',


#%%

# pd.options.display.max_columns = None
# pd.options.display.max_rows = None


loader_df = q.loader_endpoint(apikey,username,start_date,max_size)
time.sleep(2)
ondemand_df = q.ondemand_endpoint(apikey,username,start_date,max_size)
time.sleep(2)
content_df = q.content_api_endpoint(apikey,username,start_date)



#%%

writer = pd.ExcelWriter('usage_output.xlsx', engine='xlsxwriter')


# LOADER

df = pd.DataFrame(columns = ['Loader Usage', 'Date'])

df.to_excel(writer, sheet_name=username, startrow=0, index=False)

column_settings = [{'header': column} for column in loader_df.columns]
(loader_max_row, loader_max_col) = loader_df.shape
worksheet = writer.sheets[username]

if (loader_max_row or loader_max_col) == 1:
    pass
else:
    worksheet.add_table(1, 0, loader_max_row, loader_max_col - 1, {'columns': column_settings})
    worksheet.set_column(0, 2, 20) # Make the columns wider for clarity.

loader_df.to_excel(writer, sheet_name=username, startrow=2, header=False, index=False)


# OnDemand

ondemand_adj_row = loader_max_row + 4

df = pd.DataFrame(columns = ['OnDemand Usage', 'Date'])

df.to_excel(writer, sheet_name=username, startrow= ondemand_adj_row, index=False)

column_settings = [{'header': column} for column in ondemand_df.columns]
(ondemand_max_row, ondemand_max_col) = ondemand_df.shape
worksheet = writer.sheets[username]

if (ondemand_max_row or ondemand_max_col) == 1:
    pass
else:
    worksheet.add_table(ondemand_adj_row + 1, 0, ondemand_max_row + ondemand_adj_row + 1, ondemand_max_col - 1, {'columns': column_settings})
    #worksheet.set_column(0, ondemand_max_col - 1, 12)

ondemand_df.to_excel(writer, sheet_name=username, startrow=ondemand_adj_row + 2, header=False, index=False)



# Content APi

content_adj_row = loader_max_row + ondemand_max_row + 8

df = pd.DataFrame(columns = ['Content API Usage', 'Date'])

df.to_excel(writer, sheet_name=username, startrow= content_adj_row, index=False)

column_settings = [{'header': column} for column in content_df.columns]
(content_max_row, content_max_col) = content_df.shape
worksheet = writer.sheets[username]

if (content_max_row or content_max_col) == 1:
    pass
else:
    worksheet.add_table(content_adj_row + 1, 0, content_max_row + content_adj_row + 1, content_max_col - 1, {'columns': column_settings})
    #worksheet.set_column(0, content_max_col - 1, 12) # Make the columns wider for clarity.

content_df.to_excel(writer, sheet_name=username, startrow=content_adj_row + 2, header=False, index=False)



# Close the Pandas Excel writer and output the Excel file.
writer.save()

# %%

# https://www.elastic.co/guide/en/kibana/current/settings.html
# https://www.youtube.com/watch?v=mbd1YI_mzbk
# https://marcobonzanini.com/2015/02/02/how-to-query-elasticsearch-with-python/
# https://medium.com/a-layman/apm-logging-services-part-3-create-a-python-client-to-fetch-data-from-elasticsearch-532c828db784


#%%

# saving to excel
# https://xlsxwriter.readthedocs.io/working_with_pandas.html
# https://xlsxwriter.readthedocs.io/working_with_cell_notation.html#cell-notation


### FDS Reference

# https://pages.github.factset.com/clp/docs/api/native-searching-cloud/
# http://is.factset.com/rpd/summary.aspx?messageId=58289251
# https://pages.github.factset.com/clp/factset-io-addon-clp/
# https://github.factset.com/clp/python-logging-clp
# https://github.factset.com/FactSet?q=&type=&language=


#%%




# Dataframe to excel 

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('usage_output.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
loader_df.to_excel(writer, sheet_name=username)

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets[username]

# Add a header format.
header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#D7E4BC',
    'border': 1})

# Write the column headers with the defined format.
for col_num, value in enumerate(loader_df.columns.values):
    worksheet.write(0, col_num + 1, value, header_format)

# Close the Pandas Excel writer and output the Excel file.
writer.save()

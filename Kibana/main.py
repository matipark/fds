#%%

import queries as q

username_list = ['prism_kr', 'perpetual', 'yonhap_kr','mac_cs_au','Doom_KR']
start_date = 'now-14d'
max_size = 20
apikey = 'apikey 6b9ea362-bcdf-4fcc-b0a0-d693a978a7bd' 


#%%

# pd.options.display.max_columns = None
# pd.options.display.max_rows = None


#%%

#username,loader_df,ondemand_df,content_df

q.generate_excel(apikey,username_list,start_date,max_size)


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

# http://log.factset.io/manage/api-keys


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

#%%


import pandas as pd
import imp_main as p
import time


#%%

df = pd.read_excel(r'C:\Users\mpark\OneDrive - FactSet\Desktop\in_progress.xlsx')

df_na = df.dropna(subset=['Imp_rpd'])
df_keep = df.drop(df_na.index)
df_keep

max = len(df.dropna(subset=['Imp_rpd']))+1

#%%


for index, row in df_keep.iterrows():
    username = row[2]
    imp_package = row[4]
    machine_sn = row[3]
    notes = row[5]
    print (username, imp_package, machine_sn, notes)
    rpd_url = p.file_rpd(username, imp_package, machine_sn, notes)
    print (rpd_url)
    rpd_number = rpd_url[-8:]
    time.sleep (3)




# %%

#'http://is.factset.com/rpd/Summary.aspx?messageId='

rpd_list = pd.DataFrame([[123455],[2432123],[254523]], columns = ['rpd_link'])


#%%    


with pd.ExcelWriter(r'C:\Users\mpark\OneDrive - FactSet\Desktop\in_progress.xlsx', engine='openpyxl', if_sheet_exists='overlay', mode='a') as writer:  
    rpd_list.to_excel(writer, startcol = 1, startrow=max+1, header = False, index = False)






#%%

# Content APi
content_adj_row = loader_max_row + ondemand_max_row + 8

df = pd.DataFrame(columns = ['Content API Usage'])

df.to_excel(writer, sheet_name=username, startrow= content_adj_row, index=False)

column_settings = [{'header': column} for column in content_df.columns]
(content_max_row, content_max_col) = content_df.shape
worksheet = writer.sheets[username]

if (content_max_row or content_max_col) == 1:
    pass
else:
    worksheet.add_table(content_adj_row + 1, 0, content_max_row + content_adj_row + 1, content_max_col - 1, {'columns': column_settings})


content_df.to_excel(writer, sheet_name=username, startrow=content_adj_row + 2, header=False, index=False)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


#%%

#%%

# VBA Reference

# https://stackoverflow.com/questions/45105388/moving-numpy-arrays-from-vba-to-python-and-back
# https://stackoverflow.com/questions/54577459/how-to-import-pandas-into-the-python-com-object-for-vba

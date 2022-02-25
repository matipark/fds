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


rpd_list = pd.DataFrame([[123455],[2432123],[254523]], columns = ['rpd_link'])

rpd_list['rpd_link'] = rpd_list['rpd_link'].apply(lambda x: p.make_hyperlink(x))

with pd.ExcelWriter(r'C:\Users\mpark\OneDrive - FactSet\Desktop\in_progress.xlsx', engine='openpyxl', if_sheet_exists='overlay', mode='a') as writer:  
    rpd_list.to_excel(writer, startcol = 1, startrow=max, header = False, index = False)



#%%

# VBA Reference

# https://stackoverflow.com/questions/45105388/moving-numpy-arrays-from-vba-to-python-and-back
# https://stackoverflow.com/questions/54577459/how-to-import-pandas-into-the-python-com-object-for-vba

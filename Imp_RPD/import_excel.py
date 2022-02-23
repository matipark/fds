#%%


import pandas as pd
import imp_main as p
import time

#%%

df = pd.read_excel (r'C:\Users\mpark\OneDrive - FactSet\Desktop\in_progress.xlsx')


df_na = df.dropna(subset=['Imp_rpd'])
df_keep = df.drop(df_na.index)
df_keep



#%%


for index, row in df_keep.iterrows():
    username = row[2]
    imp_package = row[4]
    machine_sn = row[3]
    notes = row[5]
    print (username, imp_package, machine_sn, notes)
    time.sleep (13)
    rpd_url = p.file_rpd(username, imp_package, machine_sn, notes)
    time.sleep (13)


# %%





#'http://is.factset.com/rpd/Summary.aspx?messageId='





#%%

df_na = df.dropna(subset=['Imp_rpd'])

df_keep = df.drop(df_na.index)

df_keep

#%%
#%%

import pandas as pd
import imp_main as p
from IPython.display import display

#%%

df = pd.read_excel(r'C:\Users\mpark\OneDrive - FactSet\Desktop\Shared\KR & AU Accounts.xlsx')

df_na = df.dropna(subset=['Imp. RPD'])
df_keep = df.drop(df_na.index)
df_keep.reset_index(drop=True, inplace=True)

max = len(df.dropna(subset=['Imp. RPD']))+1
rpd_list = pd.DataFrame(columns = ['rpd_url', 'rpd_number'], index = [0, 1])

display(df_keep)

for index, row in df_keep.iterrows():
    username = str(row[10]) 
    imp_package = str(row[12])
    machine_sn = row[9]
    notes = row[13]
    print ('In progress: ' + username, imp_package, machine_sn, notes)
    rpd_url = p.file_rpd(username, imp_package, machine_sn, notes)
    print ('Success: ' + rpd_url)
    rpd_list['rpd_url'].loc[index] = rpd_url
    rpd_number = rpd_url[-8:]
    rpd_list['rpd_number'].loc[index] = rpd_number


# test
# rpd_list = pd.DataFrame([["http://is.factset.com/rpd/Summary.aspx?messageId=12300455", 12300455],["http://is.factset.com/rpd/Summary.aspx?messageId=24321123",24321123],["http://is.factset.com/rpd/Summary.aspx?messageId=25452003",25452003]], columns = ['rpd_url','rpd_number'])

rpd_list['rpd_url'] = rpd_list['rpd_number'].apply(lambda x: p.make_hyperlink(x))

with pd.ExcelWriter(r'C:\Users\mpark\OneDrive - FactSet\Desktop\in_progress.xlsx', engine='openpyxl', if_sheet_exists='overlay', mode='a') as writer:  
    rpd_list['rpd_url'].to_excel(writer, startcol = 1, startrow=max, header = False, index = False)

print('Update successful')



#%%

# VBA Reference

# https://stackoverflow.com/questions/45105388/moving-numpy-arrays-from-vba-to-python-and-back
# https://stackoverflow.com/questions/54577459/how-to-import-pandas-into-the-python-com-object-for-vba

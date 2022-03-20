#%%

import pandas as pd
import imp_main as p
from IPython.display import display

#%%

df = pd.read_excel(r'C:\Users\mpark\OneDrive - FactSet\Desktop\in_progress.xlsx')

#https://factset-my.sharepoint.com/:x:/p/mcruz02_pc/Ed34Ne0SvEVBsI9iXIOisLoBdW3rjgRfafWvpoNX496MzQ?e=4%3amfCLOq&at=9

df = pd.read_csv('https://factset-my.sharepoint.com/:x:/p/mcruz02_pc/Ed34Ne0SvEVBsI9iXIOisLoBdW3rjgRfafWvpoNX496MzQ?e=4%3amfCLOq&at=9',
                 sep='\t',
                 parse_dates=[0],
                 names=['a','b','c','d','e','f'])
print (df)


#%%



df_na = df.dropna(subset=['Imp_rpd'])
df_keep = df.drop(df_na.index)
df_keep.reset_index(drop=True, inplace=True)

max = len(df.dropna(subset=['Imp_rpd']))+1
rpd_list = pd.DataFrame(columns = ['rpd_url', 'rpd_number'], index = [0, 1])

display(df_keep)

for index, row in df_keep.iterrows():
    username = str(row[2])
    imp_package = str(row[3])
    machine_sn = row[4]
    notes = row[5]
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

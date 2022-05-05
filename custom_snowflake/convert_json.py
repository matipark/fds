#%%

import pandas as pd

#%%

file = 'C:\\Users\\mpark\\OneDrive - FactSet\\Desktop\\CTS\\Snowflake\\FSI\\FS_ESG_MSCI_20220331_new.csv'
json_file = 'C:\\Users\\mpark\\OneDrive - FactSet\\Desktop\\CTS\\Snowflake\\FSI\\FS_ESG_MSCI_20220331_Output.json'
df = pd.read_csv(file,sep=',')



# taking a look at the sample table, datatype, convert date if necessary

df.dtypes

df.info()

df['Effective Date'].astype('datetime64[ns]')

df['Effective Date'] = pd.to_datetime(df['Effective Date'], format='%Y%m%d')
df['Revision Date'] = pd.to_datetime(df['Revision Date'], format='%Y%m%d')





#%%

with open(json_file, "w") as output:
        output.write(str('JSON file created below. Please add primary key details in the format "isPK":true below type values.')+"\n")

# testing if all columns are recognized type

col_list_types = []
delimiter = ','
for col in df.columns:
    if df[col].dtypes =='object' or df[col].dtypes =='bool' or df[col].dtypes =='datetime64[ns]' or df[col].dtypes =='float64' or df[col].dtypes =='int64':
        pass
    else: col_list_types.append(col)

col_list_types_delim = delimiter.join(col_list_types)

if len(col_list_types) == 0:
    with open(json_file, "a") as output:
        output.write(str("All columns' data types are recognized.")+"\n")
else:
    with open(json_file, "a") as output:
        output.write(str("The following columns' data types are unrecognized:")
                     +str(col_list_types_delim)
                     +"\n"+"\n")

# checking columns that are null

col_list_null = []
delimiter = ','
for col in df.columns:
    if df[col].nunique()==0:
        col_list_null.append(col)
    else: pass

col_list_null_delim = delimiter.join(col_list_null)

if len(col_list_null) == 0:
    pass
else:
    with open(json_file, "a") as output:
        output.write(str("Some columns only have null values: ")
                     +str(col_list_null_delim)
                     +str(". Please confirm data type and enter manually below.")+"\n")
        

# defining PK column

col_list_pk = []
delimiter = ','
for col in df.columns:
    if df[col].is_unique==True and df[col].isnull().any()==False:
        col_list_pk.append(col)
    else: pass

col_list_pk_delim = delimiter.join(col_list_pk)

if len(col_list_pk_delim) == 0:
    pass
else:
    with open(json_file, "a") as output:
        output.write(str("Some columns only have pk values: ")
                     +str(col_list_null_delim)
                     +"\n")



# col_list_char = []
# delimiter = ','
# for col in df.columns:
#     if df[col].dtypes =='object' and df[col].map(len).nunique()==1:
#         col_list_char.append(col)
#     else: pass

# col_list_char_delim = delimiter.join(col_list_char)

# if len(col_list_char) == 0:
#     pass
# else:
#     with open(json_file, "a") as output:
#         output.write(str("The following columns were identified as CHAR: ")
#                      +str(col_list_char_delim)
#                      +str(". Please confirm if string length will always be the same; if not, update type to VARCHAR below.")+"\n")


col_list_header = []
delimiter = ','
for col in df.columns:
    if 'Unnamed:' in col:
        col_list_header.append(col)
    else: pass

col_list_header_delim = delimiter.join(col_list_header)

if len(col_list_header) == 0:
    pass
else:
    with open(json_file, "a") as output:
        output.write(str("The following columns have no header: ")
                     +str(col_list_header_delim)
                     +str(". Please add headers to the input file and rerun this script.")+"\n"+"\n")


#begin JSON creation                     
with open(json_file, "a") as output:
        output.write(str('{')+"\n"+str('"fields":[')+"\n")

for col in df.columns:
    if df[col].dtypes =='object':
        # if df[col].map(len).nunique()==1:
        #     with open(json_file, "a") as output:
        #         output.write(str('{')+"\n"+str('"name":"')+col+str('",')+"\n"+str('"type":"CHAR"')+"\n"+str('},')+"\n")
        # else:
            with open(json_file, "a") as output:
                output.write(str('{')+"\n"+str('"name":"')+col+str('",')+"\n"+str('"type":"STRING"')+"\n"+str('},')+"\n")
    elif df[col].dtypes =='bool':
            with open(json_file, "a") as output:
                output.write(str('{')+"\n"+str('"name":"')+col+str('",')+"\n"+str('"type":"BOOLEAN"')+"\n"+str('},')+"\n")
    elif df[col].dtypes =='datetime64[ns]':
            with open(json_file, "a") as output:
                output.write(str('{')+"\n"+str('"name":"')+col+str('",')+"\n"+str('"type":"DATE"')+"\n"+str('},')+"\n")
    elif df[col].dtypes =='float64' or df[col].dtypes =='int64':
            with open(json_file, "a") as output:
                output.write(str('{')+"\n"+str('"name":"')+col+str('",')+"\n"+str('"type":"NUMERIC"')+"\n"+str('},')+"\n")
    else:
        with open(json_file, "a") as output:
            output.write(str('{')+"\n"+str('"name":"')+col+str('",')+"\n"+str('"type":"UNRECOGNIZED"')+"\n"+str('},')+"\n")

# with open(json_file, 'rb+') as filehandle:
#     filehandle.seek(-3, os.SEEK_END)
#     filehandle.truncate()
    
with open(json_file, "a") as output:
        output.write("\n"+str(']')+"\n"+str('}'))

        
# %%

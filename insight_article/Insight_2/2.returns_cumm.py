#%%

import pandas as pd
import pyodbc
import time
import warnings

import loadsql #functions to load sql queries

from datetime import datetime
from IPython.display import display
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd


# connecting python with SQL 
dsn = 'SF'
connection_to_sql = pyodbc.connect('DSN={dsn_name}'.format(dsn_name = dsn))

# how_many = connection_to_sql.getinfo(pyodbc.SQL_MAX_CONCURRENT_ACTIVITIES)
# print(how_many)

#%%

bdx_board_char_type = "\'Overall Board Characteristics\'"

start_time = time.time()

r3000_query = loadsql.get_sql_q('3.bdx_sf_tr.sql',show=0,connection=dsn, skipSubsCheck=1).format(bdx_board_char_type=bdx_board_char_type)

with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    r3000_result = pd.read_sql(r3000_query,connection_to_sql)

print("Process finished --- %s seconds ---" % (time.time() - start_time))

sp500_query = loadsql.get_sql_q('3.bdx_sp50_sf_tr.sql',show=0,connection=dsn, skipSubsCheck=1).format(bdx_board_char_type=bdx_board_char_type)

with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    sp500_result = pd.read_sql(sp500_query,connection_to_sql)

print("Process finished --- %s seconds ---" % (time.time() - start_time))


r3000_mcv_query = loadsql.get_sql_q('3.bdx_sf_tr_MCV.sql',show=0,connection=dsn, skipSubsCheck=1)

with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    r3000_mcv_result = pd.read_sql(r3000_mcv_query,connection_to_sql)

print("Process finished --- %s seconds ---" % (time.time() - start_time))

sp500_mcv_query = loadsql.get_sql_q('3.bdx_sp50_sf_tr_MCV.sql',show=0,connection=dsn, skipSubsCheck=1)

with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    sp500_mcv_result = pd.read_sql(sp500_mcv_query,connection_to_sql)

print("Process finished --- %s seconds ---" % (time.time() - start_time))

r3000_pr_query = loadsql.get_sql_q('4.calc_returns_sf.sql',show=0,connection=dsn, skipSubsCheck=1).format(bdx_board_char_type=bdx_board_char_type)

with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    r3000_pr_result = pd.read_sql(r3000_pr_query,connection_to_sql)

print("Process finished --- %s seconds ---" % (time.time() - start_time))

sp500_pr_query = loadsql.get_sql_q('4.calc_sp50_returns_sf.sql',show=0,connection=dsn, skipSubsCheck=1).format(bdx_board_char_type=bdx_board_char_type)

with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    sp500_pr_result = pd.read_sql(sp500_pr_query,connection_to_sql)

print("Process finished --- %s seconds ---" % (time.time() - start_time))

final_df = pd.merge(r3000_pr_result, r3000_result, on=['FSYM_ID','DATE_YEAR'], how='inner')
final_mcv_df = pd.merge(r3000_pr_result, r3000_mcv_result, on=['FSYM_ID','DATE_YEAR'], how='inner')
sp500_final_df = pd.merge(sp500_pr_result, sp500_result, on=['FSYM_ID','DATE_YEAR'], how='inner')
sp500_final_mcv_df = pd.merge(sp500_pr_result, sp500_mcv_result, on=['FSYM_ID','DATE_YEAR'], how='inner')

# final_df[ final_df['DATE_YEAR'] == 2020]
# boolean = not final_df[final_df['DATE_YEAR'] == 2021]['FSYM_ID'].is_unique  

#%%

# calculate quintile for BDX factors

# Russell 3000
final_df['quintile_gender'] = pd.cut(final_df['BDX_GENDER_RATIO'], 5) # around mid is best, 100 means man
final_df['quintile_nationality'] = pd.cut(final_df['BDX_NATIONALITY_MIX'], 5)
final_df['quintile_quals'] = pd.cut(final_df['BDX_STDEV_QUALS'], 5)
final_df['quintile_age'] = pd.cut(final_df['BDX_STDEV_AGE'], 5)

# S&P 500
sp500_final_df['quintile_gender'] = pd.cut(sp500_final_df['BDX_GENDER_RATIO'], 5) # around mid is best, 100 means man
sp500_final_df['quintile_nationality'] = pd.cut(sp500_final_df['BDX_NATIONALITY_MIX'], 5)
sp500_final_df['quintile_quals'] = pd.cut(sp500_final_df['BDX_STDEV_QUALS'], 5)
sp500_final_df['quintile_age'] = pd.cut(sp500_final_df['BDX_STDEV_AGE'], 5)


# final_df['quintile_lst_brd'] = pd.cut(r3000_result['BDX_STDEV_LST_BRD'], 5)
# final_df['quintile_curr_lst_brd'] = pd.cut(r3000_result['BDX_STDEV_CURR_LST_BRD'], 5)

# final_df['BDX_GENDER_RATIO'].head()
# final_mcv_df['MCV_CEO_RANK'].head()


#, labels=False
#, duplicates='drop'




#%%

# calcultate market cap weights for each security by year

final_df['mcap_sum'] = final_df.groupby('DATE_YEAR')['FF_MKT_VAL'].transform('sum') # put the respective annual sum for each row
final_df['annual_mcap_weight'] = final_df['FF_MKT_VAL']/final_df['mcap_sum']
final_mcv_df['mcap_sum'] = final_mcv_df.groupby('DATE_YEAR')['FF_MKT_VAL'].transform('sum')
final_mcv_df['annual_mcap_weight'] = final_mcv_df['FF_MKT_VAL']/final_mcv_df['mcap_sum']

# multiply return by market cap weights

final_df['ann_weighted_return'] = final_df['ANN_RETURN'].mul(final_df['annual_mcap_weight'], axis=0)

final_mcv_df['ann_weighted_return'] = final_mcv_df['ANN_RETURN'].mul(final_mcv_df['annual_mcap_weight'], axis=0)

# market cap sum check

# final_df[final_df['DATE_YEAR']==2020]['annual_mcap_weight'].sum()

# r3000_result['BDX_MARKET_CAP_WEI'].sum()
# r3000_result['BDX_GENDER_RATIO'].count()

#%%

#comparing equal-weight return and mcap weighted return

print(final_mcv_df.groupby('DATE_YEAR')['ANN_RETURN'].mean().tail())
print(final_mcv_df.groupby('DATE_YEAR')['ann_weighted_return'].sum().tail())

# add up to calculate the bottom-up return by factor and year

final_df.groupby(['DATE_YEAR','quintile_gender']).sum()['ann_weighted_return'].tail(15)
final_mcv_df.groupby(['DATE_YEAR','MCV_CEO_RANK']).sum()['ann_weighted_return'].tail(15)




#%%

# Calculate cummulative return from year xxxx

factors = ['quintile_gender','quintile_nationality','quintile_quals','quintile_age']


sectors = [
'Non-Energy Minerals',
'Producer Manufacturing',
'Electronic Technology',
'Consumer Durables',
'Energy Minerals',
'Process Industries',
'Health Technology',
'Consumer Non-Durables',
'Industrial Services',
'Commercial Services',
'Distribution Services',
'Technology Services',
'Health Services',
'Consumer Services',
'Retail Trade',
'Transportation',
'Utilities',
'Finance',
'Communications'
]

ret_by_factor = {}


for i in factors:
    writer = pd.ExcelWriter('bdx_{}.xlsx'.format(i),engine='xlsxwriter')
    row = 0
    for j in sectors:
        ret_by_factor[i] = sp500_final_df[(sp500_final_df['DATE_YEAR']>2007) & (sp500_final_df['FACTSET_SECTOR_DESC'] == j)].groupby(['FACTSET_SECTOR_DESC',i]).agg({i:'size', 'ANN_RETURN':'mean'}).fillna(0).rename(columns={i:'count'}).reset_index()
        ret_by_factor[i].to_excel(writer,sheet_name='bdx_sector',startrow=row , startcol=0) 
        row = row + len(ret_by_factor[i]) + 2
        print(ret_by_factor[i])
        plt.figure()
        plt.xticks(rotation=45)
        plt.title('{}: {}'.format(i,j))
        plt.xlabel("Quintile")
        plt.ylabel("Average Annual Return")
        plt.bar(ret_by_factor[i][i].astype(str),ret_by_factor[i]['ANN_RETURN'])
        plt.savefig('./pics/{}.png'.format(j.replace(" ","_")),bbox_inches='tight')
        worksheet = writer.sheets['bdx_sector']
        worksheet.insert_image('C2','./pics/{}.png'.format(j.replace(" ","_")))
        plt.show()
        print('')
    writer.save()
    #writer.close()

#%%

factors_mcv = ['MCV_CEO_RANK','MCV_TEAM_RANK']
ret_mcv_by_factor = {}
row = 0

for i in factors_mcv:
    ret_mcv_by_factor[i] = final_mcv_df[final_mcv_df['DATE_YEAR']>2007].groupby(['FACTSET_SECTOR_DESC',i]).agg({i:'size', 'ANN_RETURN':'mean'}).fillna(0).rename(columns={i:'count','ANN_RETURN':'mean_sent'}).reset_index()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  
        print(ret_mcv_by_factor[i])
    plt.figure()
    plt.xticks(rotation=45)
    plt.bar(ret_mcv_by_factor[i][i].astype(str),ret_mcv_by_factor[i]['ANN_RETURN'])
    plt.show()
    print('')

# r3000_result.groupby('quintile_nationality').sum()[['ytd_weighted_return','1yr_weighted_return_2','2yr_weighted_return_3']]
# r3000_result.groupby('quintile_quals').sum()[['ytd_weighted_return','1yr_weighted_return_2','2yr_weighted_return_3']]

#%%


# Calculate return from year xxxx for Russell 3000

factors = ['quintile_gender','quintile_nationality','quintile_quals', 'quintile_age','quintile_time_brd','quintile_time_co']

ret_by_factor = {}
writer = pd.ExcelWriter('bdx.xlsx',engine='xlsxwriter')
row = 0

for i in factors:
    ret_by_factor[i] = final_df[final_df['DATE_YEAR']>2007].groupby(i).mean()['ANN_RETURN'].fillna(0).reset_index(name = 'ANN_RETURN')
    ret_by_factor[i].to_excel(writer,sheet_name='bdx',startrow=row , startcol=0) 
    row = row + len(ret_by_factor[i]) + 2
    print(ret_by_factor[i])
    plt.figure()
    plt.xticks(rotation=45)
    plt.title(i)
    plt.xlabel("Quintile")
    plt.ylabel("Average Annual Return")
    plt.bar(ret_by_factor[i][i].astype(str),ret_by_factor[i]['ANN_RETURN'])
    plt.savefig('{}.png'.format(i),bbox_inches='tight')
    worksheet = writer.sheets['bdx']
    worksheet.insert_image('C2','{}.png'.format(i))
    plt.show()
    print('')
writer.save()

#%%

# Calculate return from year xxxx for S&P 500

factors = ['quintile_gender','quintile_nationality','quintile_quals', 'quintile_age','quintile_time_brd','quintile_time_co']

ret_by_factor = {}
writer = pd.ExcelWriter('bdx_sp500.xlsx',engine='xlsxwriter')
row = 0

for i in factors:
    ret_by_factor[i] = sp500_final_df[sp500_final_df['DATE_YEAR']>2007].groupby(i).mean()['ANN_RETURN'].fillna(0).reset_index(name = 'ANN_RETURN')
    ret_by_factor[i].to_excel(writer,sheet_name='bdx',startrow=row , startcol=0) 
    row = row + len(ret_by_factor[i]) + 2
    print(ret_by_factor[i])
    plt.figure()
    plt.xticks(rotation=45)
    plt.title(i)
    plt.xlabel("Quintile")
    plt.ylabel("Average Annual Return")
    plt.bar(ret_by_factor[i][i].astype(str),ret_by_factor[i]['ANN_RETURN'])
    plt.savefig('{}.png'.format(i),bbox_inches='tight')
    worksheet = writer.sheets['bdx']
    worksheet.insert_image('C2','{}.png'.format(i))
    plt.show()
    print('')
writer.save()


#%%

factors_mcv = ['MCV_CEO_RANK','MCV_TEAM_RANK']
ret_mcv_by_factor = {}
writer = pd.ExcelWriter('mcv.xlsx',engine='xlsxwriter')
row = 0

for i in factors_mcv:
    ret_mcv_by_factor[i] = final_mcv_df[final_mcv_df['DATE_YEAR']>2007].groupby(i).mean()['ANN_RETURN'].fillna(0).reset_index(name = 'ANN_RETURN')
    ret_mcv_by_factor[i].to_excel(writer,sheet_name='mcv',startrow=row , startcol=0) 
    row = row + len(ret_mcv_by_factor[i]) + 2
    print(ret_mcv_by_factor[i])
    plt.figure()
    plt.xticks(rotation=45)
    plt.title(i)
    plt.xlabel("Quintile")
    plt.ylabel("Average Annual Return")
    plt.bar(ret_mcv_by_factor[i][i].astype(str),ret_mcv_by_factor[i]['ANN_RETURN'])
    plt.savefig('{}.png'.format(i),bbox_inches='tight')
    worksheet = writer.sheets['mcv']
    worksheet.insert_image('C2','{}.png'.format(i))
    plt.show()
    print('')
writer.save()


#%%

factors_mcv = ['MCV_CEO_RANK','MCV_TEAM_RANK']
ret_mcv_by_factor = {}
writer = pd.ExcelWriter('mcv_sp500.xlsx',engine='xlsxwriter')
row = 0

for i in factors_mcv:
    ret_mcv_by_factor[i] = sp500_final_mcv_df[sp500_final_mcv_df['DATE_YEAR']>2007].groupby(i).mean()['ANN_RETURN'].fillna(0).reset_index(name = 'ANN_RETURN')
    ret_mcv_by_factor[i].to_excel(writer,sheet_name='mcv',startrow=row , startcol=0) 
    row = row + len(ret_mcv_by_factor[i]) + 2
    print(ret_mcv_by_factor[i])
    plt.figure()
    plt.xticks(rotation=45)
    plt.title(i)
    plt.xlabel("Quintile")
    plt.ylabel("Average Annual Return")
    plt.bar(ret_mcv_by_factor[i][i].astype(str),ret_mcv_by_factor[i]['ANN_RETURN'])
    plt.savefig('{}.png'.format(i),bbox_inches='tight')
    worksheet = writer.sheets['mcv']
    worksheet.insert_image('C2','{}.png'.format(i))
    plt.show()
    print('')
writer.save()


#%%

# Calculate cummulative return from year xxxx

factors = ['quintile_gender','quintile_nationality','quintile_quals']
ret_by_factor = {}
writer = pd.ExcelWriter('bdx_roe.xlsx',engine='xlsxwriter')
row = 0

for i in factors:
    ret_by_factor[i] = final_df[final_df['DATE_YEAR']>2007].groupby(i).mean()['FF_ROE'].reset_index(name = 'ROE')
    ret_by_factor[i].to_excel(writer,sheet_name='bdx_roe',startrow=row , startcol=0) 
    row = row + len(ret_by_factor[i]) + 2
    print(ret_by_factor[i])
    plt.figure()
    plt.xticks(rotation=45)
    plt.title(i)
    plt.xlabel("Quintile")
    plt.ylabel("Average Annual Return")
    plt.bar(ret_by_factor[i][i].astype(str),ret_by_factor[i]['ROE'])
    plt.savefig('{}.png'.format(i),bbox_inches='tight')
    worksheet = writer.sheets['bdx_roe']
    worksheet.insert_image('C2','{}.png'.format(i))
    plt.show()
    print('')
writer.save()

#%%

factors_mcv = ['MCV_CEO_RANK','MCV_TEAM_RANK']
ret_mcv_by_factor = {}
writer = pd.ExcelWriter('mcv_roe.xlsx',engine='xlsxwriter')
row = 0

for i in factors_mcv:
    ret_mcv_by_factor[i] = final_mcv_df[final_mcv_df['DATE_YEAR']>2007].groupby(i).mean()['FF_ROE'].reset_index(name = 'ROE')
    ret_mcv_by_factor[i].to_excel(writer,sheet_name='mcv_roe',startrow=row , startcol=0) 
    row = row + len(ret_mcv_by_factor[i]) + 2
    print(ret_mcv_by_factor[i])
    plt.figure()
    plt.xticks(rotation=45)
    plt.title(i)
    plt.xlabel("Quintile")
    plt.ylabel("Average Annual Return")
    plt.bar(ret_mcv_by_factor[i][i].astype(str),ret_mcv_by_factor[i]['ROE'])
    plt.savefig('{}.png'.format(i),bbox_inches='tight')
    worksheet = writer.sheets['mcv_roe']
    worksheet.insert_image('C2','{}.png'.format(i))
    plt.show()
    print('')
writer.save()


#%%

cumm_ret_df = final_df.groupby('DATE_YEAR')['ANN_RETURN'].mean().reset_index(name ='annual_return')

cumm_ret_df = (((1 + final_df[final_df['DATE_YEAR']>2007][['DATE_YEAR','ANN_RETURN']].groupby('DATE_YEAR').mean()/100).cumprod()- 1)*100)





cumm_ret_df = (((1 + final_mcv_df[final_mcv_df['DATE_YEAR']>2017][['DATE_YEAR','ann_weighted_return']].groupby('DATE_YEAR').sum()/100).cumprod()- 1)*100)


cumm_ret_df = (((1 + final_df[final_df['DATE_YEAR']>2017][['DATE_YEAR','ann_weighted_return']].groupby('DATE_YEAR').sum()/100).cumprod()- 1)*100)

cumm_ret_df['yearly_return'] = final_df[final_df['DATE_YEAR']>2017].groupby('DATE_YEAR').sum()['ann_weighted_return']

# Or:
# df.Daily_rets.add(1).cumprod().sub(1)



#%%

# count in each one of the factors

final_df.groupby('quintile_gender')['quintile_gender'].count()
final_df.groupby('quintile_nationality')['quintile_nationality'].count()
final_df.groupby('quintile_quals')['quintile_quals'].count()

r3000_mcv_result.groupby('quintile_gender')['quintile_nationality'].count()
r3000_mcv_result.groupby('quintile_nationality')['quintile_nationality'].count()


# ranking by factor then calculate overall

#df['default_rank'] = df['Number_legs'].rank()

# %%

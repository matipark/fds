#%%

import pandas as pd
import numpy as np
import pyodbc
import os
import lxml
from bs4 import BeautifulSoup
import zipfile
import time
import glob
import datetime
import matplotlib.pyplot as plt
from IPython.display import display, Markdown,HTML
import loadsql #functions to load sql queries


# %%

# connecting python with SQL 
dsn = 'FDSLoader'
connection_to_sql = pyodbc.connect('DSN={dsn_name}'.format(dsn_name = dsn))


#%%

start_time = time.time()

# retriving all participants for the last 3 months
sql_query_1 = loadsql.get_sql_q('C:\\Github_repo\\Notes\\FDS\\xml_transcripts\\1.4.1 Retrieve All Participants from Earnings Calls in Past 3 Months.sql',show=0,connection=dsn)

df_1 = pd.read_sql(sql_query_1,connection_to_sql)

print("Process finished --- %s seconds ---" % (time.time() - start_time))

#%%

df_1.head()

#%%

# excluding people working in the company & finding analysts
analysts = df_1[df_1.person_comp_entity_id!=df_1.factset_entity_id].groupby(['factset_person_id','person_name','person_comp_name','participant_title'])[['event_id','factset_entity_id']].nunique()

# finding analysts with highest number of participation
analysts.rename(columns={'event_id':'Total Events','factset_entity_id':'Unique Companies'},inplace=True)
analysts.sort_values(['Total Events'],ascending=False).head()


# %%

# finding events with highest number of analysts participating
event_parts = df_1.groupby(['event_id','entity_proper_name','title']).factset_person_id.nunique().sort_values(ascending=False).reset_index().rename(columns={'factset_person_id':'Num Participants'})

event_parts.head()

# %%

event_parts.tail()

#%%


# archive for transcripts in the year of 2020
archive_path = 'C:\\Users\\mpark\\OneDrive - FactSet\\Documents\\Loader_app\\zips\\tr_history_2020_full_1535'

fund_ticker='SPY-US'
sd = '2020-01-01'
ed = '2020-12-31'

# Using a fund ticker as our portfolio and bring up its constituents
sql_query_2 = loadsql.get_sql_q('C:\\Github_repo\\Notes\\FDS\\xml_transcripts\\2.5.1 Retrieving an ETF Universe.sql',show=0,connection=dsn).format(fund = fund_ticker,sd=sd,ed=ed)
univ = pd.read_sql(sql_query_2,connection_to_sql,parse_dates=['startdate','enddate'])

univ.head()


# %%

entity_ids = "'"+"','".join(str(x) for x in 
                            univ.factset_entity_id.dropna().unique().tolist()) + "'"

#loading transcripts name for those ids in the portfolio
sql_query_3 = loadsql.get_sql_q('C:\\Github_repo\\Notes\\FDS\\xml_transcripts\\2.5.2 Retrieving Events for a List of Entity IDs.sql',show=0,connection=dsn).format(entity_ids = entity_ids,sd=sd,ed=ed)

event = pd.read_sql(sql_query_3,connection_to_sql)

#merge with the Universe table
event = univ.merge(event,how='inner',on='factset_entity_id')

#only include events when the company was part of the universe
event[(event.event_datetime_utc>=event.startdate)&(event.event_datetime_utc<=event.enddate)]

#del univ

event.head()

#%%

event.groupby('event_type_display_name').report_id.nunique()


# %%

#Guidance Calls and the "Corrected" Version of the Transcript
guid = event[(event.event_type_display_name=='Guidance')&
             (event.transcript_type=='C')].copy()

#this code block is constructed to handle more than one event
docs = guid.xml_filename.values.tolist() 

doc_list = [os.path.join(archive_path, a) for a in docs]
parser = lxml.etree.XMLParser(encoding='utf-8',recover=True)

print('Number of Transcripts: {}'.format(len(doc_list)))


#%%

# C:\Users\mpark\OneDrive - FactSet\Documents\Loader_app\zips\tr_history_2020_full_1535

start_time = time.time()


participants = []
body = []
for doc in doc_list:
    xml = open(doc,'rb').read()
    tree = lxml.etree.fromstring(xml,parser)
    
    doc_name = doc.split('\\')[-1]
################      
#Participants
################    
    parts = [tr for tr in set(tree.findall('.//participant',namespaces=tree.nsmap))]

    for elem in parts:
        temp = dict(elem.attrib)
        temp.update({'name':elem.text})
        temp.update({'document':doc_name})
        participants.append(temp)

################    
#Body Section
################    
    sections = [tr for tr in set(tree.findall('.//section',namespaces=tree.nsmap))]
    cnt = 1
    
    for sec in sections:
        #identify all speaker tags
        speakers =[spk for spk in sec.findall('.//speaker',namespaces=tree.nsmap)]
        
        #find the speaker id and response type
        s_id,s_type = map(list,zip(*[(sid.get('id'),sid.get('type')) for sid in speakers]))

        #replicate the section name for each row
        sec_name = [sec.values()[0]]*len(s_id)
        
        #replicate doc for each row
        doc_name_list = [doc_name]*len(s_id)       
        #turn all paragraphs for a speakers comments into a list
        text = [[par.text for par in spk.findall('.//p',namespaces=tree.nsmap)] for spk in speakers]

        #keep track of order per section 
        order = list(range(1,len(s_id)+1))
            
        #turn lists into a dictionary and then a dataframe
        body.append(pd.DataFrame.from_dict({'document':doc_name_list
                                            ,'section':sec_name
                                            ,'order':order
                                            ,'id':s_id
                                            ,'response_type':s_type
                                            ,'text':text},orient='columns'))

participants = pd.DataFrame(participants)
#order columns
participants = participants[['document','id','affiliation','affiliation_entity'
                             ,'name','entity','title','type']]
body = pd.concat(body)
#order columns
body = body[['document','section','id','response_type','text','order']]



print("Process finished --- %s seconds ---" % (time.time() - start_time))

# %%

df = participants.merge(body,on=['id','document'],how='inner')
df.sort_values(['document','section','order'],inplace=True)
df[df.type!='operator'].set_index('id').head(30)


# %%

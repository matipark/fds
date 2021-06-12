#%%

import hashlib 
import hmac 
import requests 
import json
from xml.dom import minidom

#Your FactSet Information 

username = 'FDS_DEMO_FE' #Insert your FactSet Username provided by your FactSet Account team 
serial = '410734' #Insert Serial Number tied to machine account provided by your FactSet Account

#%%


output_dir = r'C:\Users\mpark\OneDrive - FactSet\Desktop\Test\_'

#read key.txt
keyfile = r'C:\Users\mpark\OneDrive - FactSet\Desktop\FDSLoader-Windows-2.11.1.0\key2.txt'
d = {}
with open(keyfile) as f:
    for line in f:
        (k,v) = line.strip().split(": ")
        d[k] = v

#key = 'c6e5c56bf4ebe73712808e7142603a63c9b2abfcb9566e61e41b697cb69c96fb62d813ec63cd6550c20025b3af3effec3743976c1adebb6b832610d2d9b1dae9' #Insert Key from auth-factset.com 
key = d['Key']
#keyId = 'AAAB' #Insert KeyID from auth-factset.com
keyId = d['KeyId']
#counter = -7761845995145632083 #Insert Counter from auth-factset.com 
counter = int(d['Counter'])

#Compute OTP 
ba_key = bytearray.fromhex(key) 
my_int = counter.to_bytes(8, 'big', signed=True)
my_hmac = hmac.new(ba_key,msg=my_int, digestmod=hashlib.sha512) 
digested_counter = my_hmac.digest() 
otp = digested_counter.hex()

#Authenticate and retrieve session Token 
json_object = { 
'username': username, 
'keyId': keyId, 
'otp': otp , 
'serial': serial 
}

OTP_url = 'https://auth.factset.com/fetchotpv1' 
payload = json.dumps(json_object) 
header = {'Content-Type': 'application/json'}

r = requests.post(OTP_url, data=payload, headers=header)

r_key = r.headers.get(key='X-DataDirect-Request-Key') 
r_token = r.headers.get(key='X-Fds-Auth-Token')

print('DataDirect Request Key: ', r_key) 
print('Token:', r_token)

#Confirm authentication and session token work 
header = {'X-Fds-Auth-Token':r_token} 
Service_url = 'https://datadirect.factset.com/services/auth-test'

r = requests.get(Service_url,headers=header)


#update counter and write to key.txt
counter += 1
with open(r'C:\Users\mpark\OneDrive - FactSet\Desktop\FDSLoader-Windows-2.11.1.0\key2.txt','w') as f:
    f.write('KeyId: '+ keyId + '\n')
    f.write('Key: '+ key + '\n')
    f.write('Counter: '+ str(counter))

print('Status code: ', r.status_code) 
print('Status reason: ', r.reason) 
print('Message: ', r.text)
print('Counter: ', counter)




# %%


#search parameters:
sd ='20191001' #start date
ed ='20201231' #end date
payload = { 'report': 'search',

#define the request type as a search
'sd': sd,
'ed': ed,
'sources': 'SA',
'ids': 'aapl-us',
'sa_categories': 'SA_EARNINGS',
'n' : '10'
}


#Docretrieval URL used for request call
url = 'https://datadirect.factset.com/services/NewsFetch'
#Make request
r= requests.get(url,params=payload,headers=header)
print('Status Code: {:d}'.format(r.status_code))
print(r.content)
#read in XML response
doc = minidom.parseString(r.content)
search_results = doc.getElementsByTagName('RecordsReturned')
records_returned = search_results[0].firstChild.nodeValue
print ('{} transcripts found'.format(records_returned))
links = []

#Store the filename and each link to download transcripts

if int(records_returned)>0:
  records = doc.getElementsByTagName('Record')
  print(records)
  for rec in records:
    field = rec.getElementsByTagName('Field')
    for f in field:
      for attrID, attrName in f.attributes.items():
        list_doc = dict(f.attributes.items())
        if attrID == 'id' and attrName == '7011':
          links.append(list_doc['value'])

#Download transcripts to output_dir directory
for i,(l) in enumerate(links):
  url = l
  print(url)
  #query based on company and date and source
  #pass in session token
  r = requests.get(url,headers=header,stream=True)
  if r.status_code == 200:
    print (" {:d} of {:d} downloaded".format(i+1,len(links)))
  else:
    print ('Error')
  #create filename
  local_filename = output_dir + 'file_'+str(i) + '.html'

  with open(local_filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size = 1024):
      if chunk:
        f.write(chunk)



# %%

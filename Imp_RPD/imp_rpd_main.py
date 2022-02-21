
#%%

import requests

headers = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Access-Control-Request-Method': 'POST',
    'Access-Control-Request-Headers': 'content-type,x-datadirect-auth-token,x-fds-application-client,x-fds-chrome-extension,x-rpd-source',
    'Origin': 'https://rpd.factset.io',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://rpd.factset.io/',
    'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
}

response = requests.options('https://rpd.factset.com/api/v2/rpd/', headers=headers)

#%%


cookies = {
    '_gcl_au': '1.1.154918906.1618207416',
    '_ga': 'GA1.2.899032532.1618207416',
    '_fbp': 'fb.1.1618207416812.1884441893',
    '__clickidc': '161820741721012145',
    '__qca': 'P0-130876982-1618207417714',
    '_lo_uid': '195197-1618207416386-2e69d031a93d19f8',
    '__lotl': 'https%3A%2F%2Fwww.factset.com%2Fmarketplace%23%2F',
    'hubspotutk': '9dd4e35578092082f3d108b01a41bf16',
    '__hs_opt_out': 'no',
    '__lotr': 'https%3A%2F%2Fwww.google.com%2F',
    'FdsAuthScheme': 'forms',
    'FdsBrowserId': 'c22f78bc-a449-4c79-9287-62a9149eef4e',
    '_gid': 'GA1.2.2084456860.1633324788',
    '_uetvid': 'd19777209b5411ebbbbe7990fe68c7e7',
    '_pk_id.1.94d5': '34c8b5fbdac8f33b.1618885641.26.1633442432.1633401702.',
    'AccessedApplications': 'FactSet',
    '__hssrc': '1',
    'TS01742872': '01b461a0b115e432d99d3dd059a1003dbd24bcd400ddd2dde8340acc751d1fc7c6b464d2bdb91ef82040f620bb2b182ab593a8de1a67705c949eed1d2a7013d89d833141f1',
    '__hstc': '226296197.9dd4e35578092082f3d108b01a41bf16.1618207419801.1633496354813.1633500640092.63',
    '_lo_v': '272',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'Accept': 'application/json, text/plain, */*',
    'X-RPD-Source': 'RPD New UI',
    'sec-ch-ua-mobile': '?0',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'x-fds-application-client': 'chromium-extension',
    'x-fds-chrome-extension': 'lippbdnmaloigalnpfjhginenlbcjiod',
    'x-datadirect-auth-token': 'ac315a2d2d79534d',
    'Origin': 'https://rpd.factset.io',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://rpd.factset.io/',
    'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
}

data = {
  '{"Title":"fnz_au - custom feed with fx prices","Content":"<p>fx feed as custom due to wm/r retirement</p>\\n<p>': '',
  'nbsp;</p>","Severity":"Medium","Type":"Question","Private":false,"ClientDisclosed":false,"DraftId":"24535689","AtlasRelease":null,"Products":[{"Categories":null,"Id":"47602"}],"ClientsAffected":[{"Client":"646174","Type":"Individual","Name":"Peter K. Liau"}],"Entity":{"Type":"Client","Value":"646174","ClientType":"Individual","DisplayText":"Peter K. Liau"},"Questions":[]}': ''
}

# data = {
#   '{"Title":"regal_au - tick history api","Content":"<p><strong>Client credentials:': '',
#   'nbsp;</strong></p>\\n<p>': '',
#   'nbsp;</p>\\n<p>Username (.net ID):': '',
#   'nbsp;<a href': '\\"mailto:mitch.hennessy1@factset.net\\" target=\\"_blank\\" rel=\\"noopener\\">mitch.hennessy1@factset.net</a></p>\\n<p>Personal serial:',
#   'nbsp;<strong>1269748</strong></p>\\n<p>Machine serial:': '',
#   'nbsp;<strong>1276702</strong></p>\\n<p>Authentication username:': '',
#   'nbsp;<strong>REGAL_AU-1276702</strong></p>","Severity":"Medium","Type":"Question","Private":false,"ClientDisclosed":false,"DraftId":"24535658","AtlasRelease":null,"Products":[{"Categories":[{"Id":15216}],"Id":"50727"}],"ClientsAffected":[{"Client":"2075790","Type":"Individual","Name":"Mitch Hennessy"}],"Entity":{"Type":"Client","Value":"2075790","ClientType":"Individual","DisplayText":"Mitch Hennessy"},"Questions":[]}': ''
# }

response = requests.post('https://rpd.factset.com/api/v2/rpd/', headers=headers, cookies=cookies, data=data)



# %%


#%%


cookies = {
    'FdsAuthScheme': 'forms',
    'FdsBrowserId': 'c22f78bc-a449-4c79-9287-62a9149eef4e',
    'AccessedApplications': 'FactSet',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'x-fds-application-client': 'chromium-extension',
    'x-fds-chrome-extension': 'lippbdnmaloigalnpfjhginenlbcjiod',
    'x-datadirect-auth-token': 'a36e3105a1c79009',
    'Origin': 'https://rpd.factset.io',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://rpd.factset.io/',
    'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
}

data = {
  '{"Title":"npm package not working for typescript","Content":"<p>Hello team, <span class': '\\"nameSuggestion is-core_hover\\" style=\\"color: #00008b; -moz-user-select: none; font-weight: bold;\\" contenteditable=\\"false\\" data-suggestion-guid=\\"1\\" data-ismailin=\\"false\\" data-employee-id=\\"4985\\" data-cardtype=\\"employee\\">@AsaGassner</span>',
  'nbsp;</p>\\n<p>': '',
  'nbsp;</p>\\n<p>Can you kindly help with the client question just getting started with Data Monitor API?</p>\\n<p>': '',
  'nbsp;</p>\\n<p><em>It was great to see you had an npm package as we run a node backend, but unfortunately, it doesn\'t work with node.': '',
  'nbsp;</em></p>\\n<p><em>I think it was released assuming typescript would be used and needs to be compile differently for a js environment. Can you help?</em></p>\\n<p>Thanks</p>\\n<p>Matias</p>","Severity":"Medium","Type":"Question","Private":false,"ClientDisclosed":false,"DraftId":"24536147","AtlasRelease":null,"Products":[{"Categories":[{"Id":28890}],"Id":"106248"}],"AdditionalCc":[{"Id":"e_4985","OwnerType":1}],"ClientsAffected":[{"Client":"1742479","Type":"Individual","Name":"David Bankier"}],"Assignees":[],"Entity":{"Type":"Client","Value":"1742479","ClientType":"Individual","DisplayText":"David Bankier"}}': ''
}

response = requests.post('https://rpd.factset.com/api/v2/rpd/', headers=headers, cookies=cookies, data=data)

#%%

import requests

headers = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Access-Control-Request-Method': 'GET',
    'Access-Control-Request-Headers': 'x-datadirect-auth-token,x-fds-application-client,x-fds-chrome-extension',
    'Origin': 'https://rpd.factset.io',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://rpd.factset.io/',
    'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
}

params = (
    ('indexName', 'rpdproduct'),
    ('q', 'enableBQE: true AND (hasRestrictedCreator:\'false\' OR authorizedCreators:e_12149) AND ((standard implementa*) OR (standard implementa))*'),
    ('start', '0'),
    ('limit', '10'),
    ('format', 'json'),
    ('provider', 'elasticsearch'),
)

response = requests.options('https://is.factset.com/search/search.ashx', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.options('https://is.factset.com/search/search.ashx?indexName=rpdproduct&q=enableBQE:%20true%20AND%20(hasRestrictedCreator:%27false%27%20OR%20authorizedCreators:e_12149)%20AND%20((standard%20implementa*)%20OR%20(standard%20implementa))*&start=0&limit=10&format=json&provider=elasticsearch', headers=headers)
# %%
import requests

headers = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Access-Control-Request-Method': 'GET',
    'Access-Control-Request-Headers': 'x-datadirect-auth-token,x-fds-application-client,x-fds-chrome-extension',
    'Origin': 'https://rpd.factset.io',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://rpd.factset.io/',
    'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
}

response = requests.options('https://is.factset.com//CRMHovercard/areas/individual/resources/individual.js', headers=headers)

#%%

import requests

headers = {
    'authority': 'sentry-public.factset.io',
    'accept': '*/*',
    'access-control-request-method': 'POST',
    'access-control-request-headers': 'x-datadirect-auth-token,x-fds-application-client,x-fds-chrome-extension',
    'origin': 'https://rpd.factset.io',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-fetch-dest': 'empty',
    'referer': 'https://rpd.factset.io/',
    'accept-language': 'en-US,en;q=0.9,ko;q=0.8',
}

params = (
    ('sentry_key', '2a6cdfc80fae4fc89628783c7e2bd113'),
    ('sentry_version', '7'),
)

response = requests.options('https://sentry-public.factset.io/api/432/store/', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.options('https://sentry-public.factset.io/api/432/store/?sentry_key=2a6cdfc80fae4fc89628783c7e2bd113&sentry_version=7', headers=headers)

# %%

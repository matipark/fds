#%%

import requests
import pandas as pd
import json
import time 
from datetime import date
from tqdm import tqdm

today = date.today().strftime("%Y%m%d")

username = 'mac_cs_au'
max_size = 5
start_date = 'now-30d'
apikey = 'apikey 6b9ea362-bcdf-4fcc-b0a0-d693a978a7bd' 

#%%

def content_api_endpoint(apikey,username,start_date):

    headers = {
        'Authorization': apikey,
        'content-type': 'application/json',
    }

    query = {
        "aggs": {
            "2": {
            "terms": {
                "field": "@fields.additionalInfo.endpoint.raw",
                "size": 27,
                "order": {
                "_count": "desc"
                }
            }
            }
        },
        # "size": 0,
        # "version": 'true',
        # "_source": {
        #     "excludes": []
        # },
        # "stored_fields": [
        #     "*"
        # ],
        # "script_fields": {},
        # "docvalue_fields": [
        #     {
        #     "field": "@timestamp",
        #     "format": "date_time"
        #     }
        # ],
        "query": {
            "bool": {
            "must": [
                {
                "match_phrase": {
                    "@fields.user": {
                    "query": username
                    }
                }
                },
                {
                "range": {
                    "@timestamp": {
                    "gte": start_date,
                    "lte": 'now',
                    }
                }
                }
            ],
            "filter": [
                {
                "match_all": {}
                },
                {
                "match_all": {}
                },
                {
                "bool": {
                    "filter": [
                    {
                        "bool": {
                        "should": [
                            {
                            "exists": {
                                "field": "@fields.additionalInfo.endpoint"
                            }
                            }
                        ],
                        "minimum_should_match": 1
                        }
                    },
                    {
                        "bool": {
                        "must_not": {
                            "bool": {
                            "should": [
                                {
                                "bool": {
                                    "should": [
                                    {
                                        "match": {
                                        "@fields.userType": "EMPLOYEE"
                                        }
                                    }
                                    ],
                                    "minimum_should_match": 1
                                }
                                },
                                {
                                "bool": {
                                    "should": [
                                    {
                                        "bool": {
                                        "should": [
                                            {
                                            "match": {
                                                "@fields.userTYPE": "INTERNAL"
                                            }
                                            }
                                        ],
                                        "minimum_should_match": 1
                                        }
                                    },
                                    {
                                        "bool": {
                                        "should": [
                                            {
                                            "bool": {
                                                "should": [
                                                {
                                                    "query_string": {
                                                    "fields": [
                                                        "@fields.user"
                                                    ],
                                                    "query": "FDS*"
                                                    }
                                                }
                                                ],
                                                "minimum_should_match": 1
                                            }
                                            },
                                            {
                                            "bool": {
                                                "should": [
                                                {
                                                    "bool": {
                                                    "should": [
                                                        {
                                                        "match": {
                                                            "@fields.userState": "MORPHED"
                                                        }
                                                        }
                                                    ],
                                                    "minimum_should_match": 1
                                                    }
                                                },
                                                {
                                                    "bool": {
                                                    "should": [
                                                        {
                                                        "match": {
                                                            "@fields.userType": "SYSTEM"
                                                        }
                                                        }
                                                    ],
                                                    "minimum_should_match": 1
                                                    }
                                                }
                                                ],
                                                "minimum_should_match": 1
                                            }
                                            }
                                        ],
                                        "minimum_should_match": 1
                                        }
                                    }
                                    ],
                                    "minimum_should_match": 1
                                }
                                }
                            ],
                            "minimum_should_match": 1
                            }
                        }
                        }
                    }
                    ]
                }
                }
            ],
            "should": [],
            "must_not": []
            }
        },
        "highlight": {
            "pre_tags": [
            "@kibana-highlighted-field@"
            ],
            "post_tags": [
            "@/kibana-highlighted-field@"
            ],
            "fields": {
            "*": {}
            },
            "fragment_size": 2147483647
        }
    }

    response = requests.post('https://log.factset.io/api/search/native/cts_content_proxy/_search', headers=headers, data = json.dumps(query))
    json_response = response.json()['aggregations']['2']['buckets']
    if len(json_response) == 0:
        final_response = pd.DataFrame(["no data available for given credentials"], columns=['message'])
    else:
        final_response = pd.json_normalize(json_response)
        final_response.insert(0 ,'username', username)

    return final_response

#%%


def ondemand_endpoint(apikey,username,start_date,max_size):

    headers = {
        'Authorization': apikey,
        'content-type': 'application/json',
    }

    query = {
    "version": 'true',
    "size": max_size,
    "sort": [
        {
        "@timestamp": {
            "order": "desc",
            "unmapped_type": "boolean"
        }
        }
    ],
    # "_source": {
    #     "excludes": []
    # },
    # "stored_fields": [
    #     "*"
    # ],
    # "script_fields": {},
    # "docvalue_fields": [
    #     {
    #     "field": "@timestamp",
    #     "format": "date_time"
    #     }
    # ],
    "query": {
        "bool": {
        "must": [
            {
            "query_string": {
                "query": "(@fields.rspCode:[200 TO 299]) OR (@fields.rspCode:[300 TO 399]) OR (@fields.rspCode:[400 TO 499]) OR (@fields.rspCode:[500 TO 599]) OR (@fields.rspCode:>=600 OR _missing_:\"@fields.rspCode\")",
                "analyze_wildcard": 'true',
                "default_field": "*"
            }
            },
            {
            "query_string": {
                "query": "@type: lima",
                "analyze_wildcard": 'true',
                "default_field": "*"
            }
            },
            {
            "match_phrase": {
                "@fields.hdrHost.raw": {
                "query": "datadirect.factset.com"
                }
            }
            },
            {
            "bool": {
                "should": [
                {
                    "match_phrase": {
                    "@fields.service.raw": "fastfetch"
                    }
                },
                {
                    "match_phrase": {
                    "@fields.service.raw": "datafetch"
                    }
                }
                ],
                "minimum_should_match": 1
            }
            },
            {
            "match_phrase": {
                "@fields.user": {
                "query": username
                }
            }
            },
            {
                "range": {
                    "@timestamp": {
                    "gte": start_date,
                    "lte": 'now',
                    }
                }
            }
        ],
        "filter": [],
        "should": [],
        "must_not": []
        }
    }
    }

    response = requests.post('https://log.factset.io/api/search/native/cauth/_search', headers=headers, data = json.dumps(query))
    json_response = response.json()['hits']['hits']
    if len(json_response) == 0:
        final_response = pd.DataFrame(["no data available for given credentials"], columns=['message'])
    else:
        final_response = pd.json_normalize(json_response).drop(['_index','_type','_id','_version','_score','sort','_source.@type','_source.@fields.beRspHdrXFdsaBackendPath','_source.@fields.beHdrXLimaCreated','_source.@fields.beHdrXLimasigDsa1024','_source.@fields.beRspHdrServer','_source.@fields.userState','_source.@fields.feHost','_source.@fields.beHdrForwarded','_source.@fields.connAvailable','_source.@fields.reqThreadActive','_source.@fields.beRspHdrContentType','_source.@fields.beRspHdrXFdsaRequestKey','_source.@fields.hdrAcceptEncoding','_source.@fields.hdrAuthorization','_source.@fields.beHdrXLimaUserstate','_source.@fields.beHdrXLimaOriginalUsername','_source.@fields.resThreadPoolSize','_source.@fields.level','_source.@fields.beHdrXLimaUsername','_source.@fields.beRspHdrVia','_source.@fields.connLeased','_source.@fields.beHdrXLimaExpiration','_source.@fields.beHdrXLimaUsertype','_source.@fields.beHdrXLimaSerial','_source.@fields.connPending','_source.@fields.resThreadActive','_source.@fields.beHdrConnection','_source.@fields.beRspHdrConnection','_source.@fields.chainId','_source.@fields.beRspHdrXFdsaBackendHostPort','_source.@fields.beHdrUserAgent','_source.@fields.beHdrXFdsaRequestKey','_source.@fields.originalUser','_source.@fields.serverName','_source.@fields.rspHdrXDatadirectRequestKey','_source.@fields.hdrContentType','_source.@fields.hdrConnection','_source.@fields.beHdrXLimaOriginalSerial','_source.@fields.connMax','_source.@fields.beRspHdrContentEncoding','_source.@fields.beRspContentLength','_source.@fields.rspContentLength','_source.@fields.beHdrAcceptEncoding','_source.@fields.beRspTime','_source.@fields.contentLength','_source.@fields.beRspHdrContentLength','_source.@fields.hdrContentLength','_source.@fields.method','_source.@fields.authUser'], axis=1, errors='ignore')

    return final_response

# final_response.info()

#%%

#ondemand_endpoint(apikey,username,start_date)


#%%


def loader_endpoint(apikey,username,start_date,max_size):

    headers = {
        'Authorization': apikey,
        'content-type': 'application/json',
    }

    query = {
        "version": 'true',
        "size": max_size,
        "sort": [
            {
            "@timestamp": {
                "order": "desc",
                "unmapped_type": "boolean"
            }
            }
        ],
        # "_source": {
        #     "excludes": []
        # },
        # "stored_fields": [
        #     "*"
        # ],
        # "script_fields": {},
        # "docvalue_fields": [
        #     {
        #     "field": "@timestamp",
        #     "format": "date_time"
        #     }
        # ],
        "query": {
            "bool": {
            "must": [
                # {
                # "query_string": {
                #     "query": "(@fields.statusCode:0) OR (@fields.statusCode:1) OR (@fields.statusCode:2)",
                #     "analyze_wildcard": 'true',
                #     "default_field": "*"
                # }
                # },
                # {
                # "match_all": {}
                # },
                {
                "match_phrase": {
                    "@fields.type": {
                    "query": "dflEnd" # narrows down to only final results
                    }
                }
                },
                {
                "match_phrase": {
                    "@fields.user": {
                    "query": username
                    }
                }
                },
                {
                    "range": {
                        "@timestamp": {
                        "gte": start_date,
                        "lte": 'now',
                        }
                    }
                }
            ],
            # "filter": [],
            # "should": [],
            # "must_not": [
                # {
                # "match_phrase": {
                #     "@fields.user": {
                #     "query": "(fds_demo_us,fts_tstprd_b,fdsqar_c,fds_of_sdf)"
                #     }
                # }
                # },
                # {
                # "query_string": {
                #     "query": "@fields.hostname:container*",
                #     "analyze_wildcard": 'true',
                #     "default_field": "*"
                # }
                # }
            #]
        }
    }
    }


    response = requests.post('https://log.factset.io/api/search/native/df_loader/_search', headers=headers, data = json.dumps(query))
    json_response = response.json()['hits']['hits']
    if len(json_response) == 0:
        final_response = pd.DataFrame(["no data available for given credentials"], columns=['message'])
    else:
        final_response = pd.json_normalize(json_response).drop(['_index','_type','_id','_version','_score','sort','_source.@fields.chainId','_source.@fields.compressed','_source.@fields.keyCounter','_source.@fields.isOnDocker','_source.@fields.maxParallelLimit','_source.@fields.userType','_source.@fields.OracleSingleUser','_source.@fields.loaderUser','_source.@fields.timeStamp','_source.@fields.endTime','_source.@fields.type','_source.@fields.user','_source.@fields.dbAuthType','_source.@fields.userState','_source.@fields.hostname','_source.@fields.originalSerial','_source.@timestamp'], axis=1, errors='ignore')

    return final_response



# len(final)
# len(final.columns)
# final_response.info()

#%%


def generate_excel(apikey,username_list,start_date,max_size):

    writer = pd.ExcelWriter('usage_output_{}.xlsx'.format(today), engine='xlsxwriter') #opening excel file

    for username in tqdm(username_list):    

        loader_df = loader_endpoint(apikey,username,start_date,max_size)
        time.sleep(2)
        ondemand_df = ondemand_endpoint(apikey,username,start_date,max_size)
        time.sleep(2)
        content_df = content_api_endpoint(apikey,username,start_date)

        # LOADER
        
        df = pd.DataFrame(columns = ['Loader Usage'])

        df.to_excel(writer, sheet_name=username, startrow=0, index=False)

        column_settings = [{'header': column} for column in loader_df.columns]
        (loader_max_row, loader_max_col) = loader_df.shape
        worksheet = writer.sheets[username]

        if (loader_max_row or loader_max_col) == 1:
            worksheet.set_column(0, 1, 20)
            worksheet.set_column(1, 2, 30) # Make the columns wider for clarity.
        else:
            worksheet.add_table(1, 0, loader_max_row, loader_max_col - 1, {'columns': column_settings})
            worksheet.set_column(0, 1, 20)
            worksheet.set_column(1, 2, 30) # Make the columns wider for clarity.

        loader_df.to_excel(writer, sheet_name=username, startrow=2, header=False, index=False)


        # OnDemand
        ondemand_adj_row = loader_max_row + 4

        df = pd.DataFrame(columns = ['OnDemand Usage'])

        df.to_excel(writer, sheet_name=username, startrow= ondemand_adj_row, index=False)

        column_settings = [{'header': column} for column in ondemand_df.columns]
        (ondemand_max_row, ondemand_max_col) = ondemand_df.shape
        worksheet = writer.sheets[username]

        if (ondemand_max_row or ondemand_max_col) == 1:
            pass
        else:
            worksheet.add_table(ondemand_adj_row + 1, 0, ondemand_max_row + ondemand_adj_row + 1, ondemand_max_col - 1, {'columns': column_settings})
            #worksheet.set_column(0, ondemand_max_col - 1, 12)

        ondemand_df.to_excel(writer, sheet_name=username, startrow=ondemand_adj_row + 2, header=False, index=False)



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
            #worksheet.set_column(0, content_max_col - 1, 12) # Make the columns wider for clarity.

        content_df.to_excel(writer, sheet_name=username, startrow=content_adj_row + 2, header=False, index=False)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()



#%%
# https://note.nkmk.me/en/python-pandas-len-shape-size/
# https://stackoverflow.com/questions/49188960/how-to-show-all-of-columns-name-on-pandas-dataframe
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

    required_columns = ['_source.@fields.user','_source.@fields.serial','_source.@timestamp','_source.@source_host','_source.@fields.reqThreadPoolMaxSize','_source.@fields.rspHdrContentLength','_source.@fields.rspTime','_source.@fields.rspHdrContentType','_source.@fields.warnings','_source.@fields.hdrHost','_source.@fields.beRspStatusReason','_source.@fields.reqMax','_source.@fields.rspHdrDate','_source.@fields.beUrl','_source.@fields.beHdrXFdsaProxyOrigClientAddr','_source.@fields.beHdrXTlsProtocol','_source.@fields.rspHdrContentEncoding','_source.@fields.beRspCode','_source.@fields.beContentLength','_source.@fields.beMethod','_source.@fields.beHdrXForwardedFor','_source.@fields.rspStatusReason','_source.@fields.duration','_source.@fields.clientIp','_source.@fields.hdrXTlsProtocol','_source.@fields.hdrUserAgent','_source.@fields.beHttpVer','_source.@fields.rspCode','_source.@fields.beRspHdrXFdsaLabel','_source.@fields.beHdrHost','_source.@fields.url','_source.@fields.reqThreadPoolSize','_source.@fields.service','_source.@fields.resThreadPoolMaxSize','_source.@fields.rspHdrKeepAlive','_source.@fields.hdrXForwardedFor','_source.@fields.rspHdrConnection','_source.@fields.reqActive','_source.@fields.httpVer']

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
        final_response_all = pd.json_normalize(json_response)
        final_response = final_response_all.reindex(columns = required_columns)

    return final_response

# final_response.info()

#%%

#ondemand_endpoint(apikey,username,start_date)


#%%


def loader_endpoint(apikey,username,start_date,max_size):

    required_columns = ['_source.@fields.originalUser','_source.@fields.serial','_source.@fields.startTime','_source.@fields.totalLocalDiskSpace','_source.@fields.statusCode','_source.@fields.databaseVersion','_source.@fields.keyId','_source.@fields.characterSet','_source.@fields.statusDesc','_source.@fields.totalMemory','_source.@fields.os','_source.@fields.databaseType','_source.@fields.isDownloadOnly','_source.@fields.totalDatabaseSpace','_source.@fields.freeLocalDiskSpace','_source.@fields.atomicRebuild','_source.@fields.level','_source.@fields.freeDatabaseSpace','_source.@fields.remoteDirSet','_source.@fields.loaderVersion','_source.@fields.DSNName','_source.@source_host']

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
        final_response_all = pd.json_normalize(json_response)
        final_response = final_response_all.reindex(columns = required_columns)

    return final_response

# len(final)
# len(final.columns)
# final_response.info()

#%%


def generate_excel(apikey,username_list,start_date,max_size):

    writer = pd.ExcelWriter('usage_output_{}.xlsx'.format(today), engine='xlsxwriter') #opening excel file

    for username in tqdm(username_list):    

        loader_df = loader_endpoint(apikey,username,start_date,max_size)
        time.sleep(3)
        ondemand_df = ondemand_endpoint(apikey,username,start_date,max_size)
        time.sleep(3)
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
            pass # pass if there's no data
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
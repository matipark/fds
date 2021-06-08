#%%

import requests
import pandas as pd
import json

serial = 939536 #1215045 #1137568
username = 'PERPETUAL' #'yonhap_kr' #'tradingview' #'PERPETUAL'
max_size = 5
start_date = 'now-30d'
apikey = 'apikey 6b9ea362-bcdf-4fcc-b0a0-d693a978a7bd' #'apikey a8b298e2-5fc6-4fb5-a6a7-cf22267ba9ab',


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
        final_response = pd.json_normalize(json_response)

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
        final_response = pd.json_normalize(json_response)

    return final_response


# len(final)
# len(final.columns)
# final.info()

#%%


#%%
# https://note.nkmk.me/en/python-pandas-len-shape-size/
# https://stackoverflow.com/questions/49188960/how-to-show-all-of-columns-name-on-pandas-dataframe
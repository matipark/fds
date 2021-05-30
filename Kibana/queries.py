#%%

import requests
import json

#%%

def content_api_endpoint(username,start_date):

    headers = {
        'Authorization': 'apikey 6b9ea362-bcdf-4fcc-b0a0-d693a978a7bd',
        #'Authorization': 'apikey a8b298e2-5fc6-4fb5-a6a7-cf22267ba9ab',
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
        "size": 0,
        "version": 'true',
        "_source": {
            "excludes": []
        },
        "stored_fields": [
            "*"
        ],
        "script_fields": {},
        "docvalue_fields": [
            {
            "field": "@timestamp",
            "format": "date_time"
            }
        ],
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

    return response
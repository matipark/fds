#%%
import requests
import json

# %%


# https://www.elastic.co/guide/en/kibana/current/settings.html
# https://www.youtube.com/watch?v=mbd1YI_mzbk
# https://marcobonzanini.com/2015/02/02/how-to-query-elasticsearch-with-python/
# https://medium.com/a-layman/apm-logging-services-part-3-create-a-python-client-to-fetch-data-from-elasticsearch-532c828db784


### FDS Reference

# https://pages.github.factset.com/clp/docs/api/native-searching-cloud/
# http://is.factset.com/rpd/summary.aspx?messageId=58289251
# https://pages.github.factset.com/clp/factset-io-addon-clp/
# https://github.factset.com/clp/python-logging-clp
# https://github.factset.com/FactSet?q=&type=&language=

# %%


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
              "query": "haloinv"
            }
          }
        },
        {
          "range": {
            "@timestamp": {
              "gte": 'now-168h',
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

response.json()

# %%


query = {
  "aggs": {
    "2": {
      "terms": {
        "field": "@fields.rspCode",
        "size": 15,
        "order": {
          "_count": "desc"
        }
      }
    }
  },
  "size": 0,
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
              "query": "haloinv"
            }
          }
        },
        {
          "range": {
            "@timestamp": {
              "gte": 'now-168h',
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
          "bool": {
            "should": [
              {
                "query_string": {
                  "fields": [
                    "@fields.service.raw"
                  ],
                  "query": "cts\\-content\\-*"
                }
              }
            ],
            "minimum_should_match": 1
          }
        }
      ],
      "should": [],
      "must_not": []
    }
  }
}


query = {}


response = requests.post('https://log.factset.io/api/search/native/cauth/_search', headers=headers, data = json.dumps(query))

a = response.json()


# %%

a['aggregations']['2']['buckets']

# %%

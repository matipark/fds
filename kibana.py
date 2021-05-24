#%%
import requests
import json
s = requests.Session()


headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://log.factset.io/',
    'Accept-Language': 'en-US,en;q=0.9',
    'If-None-Match': 'W/^\\^988-jCQ9+HzcH+wfQTZazpXJ1w^\\^',
}

response = s.get('http://log.factset.io/authenticate', headers=headers, verify=False)


#%%


headers = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Access-Control-Request-Method': 'GET',
    'Access-Control-Request-Headers': 'auth0-client,authorization,content-type',
    'Origin': 'http://log.factset.io',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'http://log.factset.io/',
    'Accept-Language': 'en-US,en;q=0.9',
}

response = s.options('https://log.identity.factset.io/userinfo', headers=headers, verify=False)

response.text


#%%



headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIyYTdjMWFiNi0zZjhjLTRmNTUtNWFmNS03NzQwY2JkOTMyOTIiLCJkaXN0aW5ndWlzaGVkTmFtZSI6IkNOPU1hdGlhcyBQYXJrLE9VPVVzZXJzLE9VPUhvbmcgS29uZyxPVT1Bc2lhIFBhY2lmaWMsT1U9Q29ycG9yYXRlLERDPXBjLERDPWZhY3RzZXQsREM9Y29tIiwiZW1haWwiOiJtcGFya0BmYWN0c2V0LmNvbSIsImV4cCI6MTYyMTY3MzA3MywiZmFtaWx5X25hbWUiOiJQYXJrIiwiZ2VuZGVyIjoiIiwiZ2l2ZW5fbmFtZSI6IlNhbmcgSm9vbiIsImlhdCI6MTYyMTY3MjE3MywiaWRlbnRpdGllcyI6W3siY29ubmVjdGlvbiI6IkVtcGxveWVlcyIsImlzU29jaWFsIjp0cnVlLCJwcm92aWRlciI6ImFkIiwidXNlcl9pZCI6IjEyMTQ5In1dLCJpc3MiOiJodHRwczovL2xvZy5pZGVudGl0eS5mYWN0c2V0LmlvLyIsImxvY2FsZSI6IkhLIiwibmFtZSI6Ik1hdGlhcyBQYXJrIiwibmlja25hbWUiOiJtcGFyayIsInBpY3R1cmUiOiJodHRwczovL2lzLmZhY3RzZXQuY29tL3NlcnZpY2VzL2VtcGxveWVlaW1hZ2UuYXNoeD9FbXBsb3llZUlkPTEyMTQ5XHUwMDI2d2lkdGg9ODBcdTAwMjZoZWlnaHQ9ODAiLCJzdWIiOiJhZHwxMjE0OSIsInVwZGF0ZWRfYXQiOiIyMDIxLTA1LTIyVDA4OjE0OjIxLjAwNTc1OVoiLCJ1c2VyX2lkIjoiYWR8MTIxNDkiLCJ1c2VybmFtZSI6Im1wYXJrIn0.VHzKnYTAaMBBuhmO26FJzK65nUg8qbY3F0eG2szMSEY',
    'kbn-version': '6.4.2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Referer': 'http://log.factset.io/search/v6/app/kibana',
    'Accept-Language': 'en-US,en;q=0.9',
    'If-None-Match': 'W/^\\^14a-q4IG2/zewBXDXRLMNPtcIQ^\\^',
}

response = s.get('http://log.factset.io/api/config', headers=headers, verify=False)


#%%

cookies = {
    'session': 's^%^3Aj^%^3A^%^7B^%^22user^%^22^%^3A^%^7B^%^22type^%^22^%^3A^%^22user^%^22^%^2C^%^22id^%^22^%^3A^%^22mpark^%^22^%^2C^%^22name^%^22^%^3A^%^22mpark^%^22^%^2C^%^22displayName^%^22^%^3A^%^22Matias^%^20Park^%^22^%^2C^%^22distinguishedName^%^22^%^3A^%^22CN^%^3DMatias^%^20Park^%^2COU^%^3DUsers^%^2COU^%^3DHong^%^20Kong^%^2COU^%^3DAsia^%^20Pacific^%^2COU^%^3DCorporate^%^2CDC^%^3Dpc^%^2CDC^%^3Dfactset^%^2CDC^%^3Dcom^%^22^%^2C^%^22employeeId^%^22^%^3A^%^2212149^%^22^%^2C^%^22email^%^22^%^3A^%^22mpark^%^40factset.com^%^22^%^2C^%^22isUser^%^22^%^3Atrue^%^2C^%^22isAdmin^%^22^%^3Afalse^%^2C^%^22roles^%^22^%^3A^%^7B^%^22member^%^22^%^3A^%^7B^%^22trusted^%^22^%^3Atrue^%^2C^%^22user^%^22^%^3Atrue^%^7D^%^2C^%^22owner^%^22^%^3A^%^7B^%^7D^%^7D^%^7D^%^2C^%^22version^%^22^%^3A2^%^7D.OCEU84^%^2FVkOICGTlQWHfo^%^2BQIlFpOL^%^2FlMR7Pf^%^2B1iKfr9w',
}

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIyYTdjMWFiNi0zZjhjLTRmNTUtNWFmNS03NzQwY2JkOTMyOTIiLCJkaXN0aW5ndWlzaGVkTmFtZSI6IkNOPU1hdGlhcyBQYXJrLE9VPVVzZXJzLE9VPUhvbmcgS29uZyxPVT1Bc2lhIFBhY2lmaWMsT1U9Q29ycG9yYXRlLERDPXBjLERDPWZhY3RzZXQsREM9Y29tIiwiZW1haWwiOiJtcGFya0BmYWN0c2V0LmNvbSIsImV4cCI6MTYyMTY3MzA3MywiZmFtaWx5X25hbWUiOiJQYXJrIiwiZ2VuZGVyIjoiIiwiZ2l2ZW5fbmFtZSI6IlNhbmcgSm9vbiIsImlhdCI6MTYyMTY3MjE3MywiaWRlbnRpdGllcyI6W3siY29ubmVjdGlvbiI6IkVtcGxveWVlcyIsImlzU29jaWFsIjp0cnVlLCJwcm92aWRlciI6ImFkIiwidXNlcl9pZCI6IjEyMTQ5In1dLCJpc3MiOiJodHRwczovL2xvZy5pZGVudGl0eS5mYWN0c2V0LmlvLyIsImxvY2FsZSI6IkhLIiwibmFtZSI6Ik1hdGlhcyBQYXJrIiwibmlja25hbWUiOiJtcGFyayIsInBpY3R1cmUiOiJodHRwczovL2lzLmZhY3RzZXQuY29tL3NlcnZpY2VzL2VtcGxveWVlaW1hZ2UuYXNoeD9FbXBsb3llZUlkPTEyMTQ5XHUwMDI2d2lkdGg9ODBcdTAwMjZoZWlnaHQ9ODAiLCJzdWIiOiJhZHwxMjE0OSIsInVwZGF0ZWRfYXQiOiIyMDIxLTA1LTIyVDA4OjE0OjIxLjAwNTc1OVoiLCJ1c2VyX2lkIjoiYWR8MTIxNDkiLCJ1c2VybmFtZSI6Im1wYXJrIn0.VHzKnYTAaMBBuhmO26FJzK65nUg8qbY3F0eG2szMSEY',
    'kbn-version': '6.4.2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'content-type': 'application/x-ndjson',
    'Origin': 'http://log.factset.io',
    'Referer': 'http://log.factset.io/search/v6/app/kibana',
    'Accept-Language': 'en-US,en;q=0.9',
}


uri = "http://log.factset.io/search/v6/elasticsearch/_msearch"

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
              "gte": 1619080080076,
              "lte": 1621672080076,
              "format": "epoch_millis"
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



    

response = s.post('http://log.factset.io/search/v6/elasticsearch/_msearch', headers=headers, cookies=cookies, json = query)

response.json()


# %%

import requests

cookies = {
    'session': 's%3Aj%3A%7B%22user%22%3A%7B%22type%22%3A%22user%22%2C%22id%22%3A%22mpark%22%2C%22name%22%3A%22mpark%22%2C%22displayName%22%3A%22Matias%20Park%22%2C%22distinguishedName%22%3A%22CN%3DMatias%20Park%2COU%3DUsers%2COU%3DHong%20Kong%2COU%3DAsia%20Pacific%2COU%3DCorporate%2CDC%3Dpc%2CDC%3Dfactset%2CDC%3Dcom%22%2C%22employeeId%22%3A%2212149%22%2C%22email%22%3A%22mpark%40factset.com%22%2C%22isUser%22%3Atrue%2C%22isAdmin%22%3Afalse%2C%22roles%22%3A%7B%22member%22%3A%7B%22trusted%22%3Atrue%2C%22user%22%3Atrue%7D%2C%22owner%22%3A%7B%7D%7D%7D%2C%22version%22%3A2%7D.OCEU84%2FVkOICGTlQWHfo%2BQIlFpOL%2FlMR7Pf%2B1iKfr9w',
}

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIyYTdjMWFiNi0zZjhjLTRmNTUtNWFmNS03NzQwY2JkOTMyOTIiLCJkaXN0aW5ndWlzaGVkTmFtZSI6IkNOPU1hdGlhcyBQYXJrLE9VPVVzZXJzLE9VPUhvbmcgS29uZyxPVT1Bc2lhIFBhY2lmaWMsT1U9Q29ycG9yYXRlLERDPXBjLERDPWZhY3RzZXQsREM9Y29tIiwiZW1haWwiOiJtcGFya0BmYWN0c2V0LmNvbSIsImV4cCI6MTYyMTY2NDIyMSwiZmFtaWx5X25hbWUiOiJQYXJrIiwiZ2VuZGVyIjoiIiwiZ2l2ZW5fbmFtZSI6IlNhbmcgSm9vbiIsImlhdCI6MTYyMTY2MzMyMSwiaWRlbnRpdGllcyI6W3siY29ubmVjdGlvbiI6IkVtcGxveWVlcyIsImlzU29jaWFsIjp0cnVlLCJwcm92aWRlciI6ImFkIiwidXNlcl9pZCI6IjEyMTQ5In1dLCJpc3MiOiJodHRwczovL2xvZy5pZGVudGl0eS5mYWN0c2V0LmlvLyIsImxvY2FsZSI6IkhLIiwibmFtZSI6Ik1hdGlhcyBQYXJrIiwibmlja25hbWUiOiJtcGFyayIsInBpY3R1cmUiOiJodHRwczovL2lzLmZhY3RzZXQuY29tL3NlcnZpY2VzL2VtcGxveWVlaW1hZ2UuYXNoeD9FbXBsb3llZUlkPTEyMTQ5XHUwMDI2d2lkdGg9ODBcdTAwMjZoZWlnaHQ9ODAiLCJzdWIiOiJhZHwxMjE0OSIsInVwZGF0ZWRfYXQiOiIyMDIxLTA1LTIyVDA1OjQyOjUzLjU1MDg1MVoiLCJ1c2VyX2lkIjoiYWR8MTIxNDkiLCJ1c2VybmFtZSI6Im1wYXJrIn0.JjRCPYkOwy-qkAXpnIBAcMQcxjBDxubjU6BprCWSzLo',
    'kbn-version': '6.4.2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'content-type': 'application/x-ndjson',
    'Origin': 'http://log.factset.io',
    'Referer': 'http://log.factset.io/search/v6/app/kibana',
    'Accept-Language': 'en-US,en;q=0.9',
}

data = '${"index":"cauth","ignore_unavailable":true,"timeout":60000,"preference":1621663317737}\\n{"aggs":{"2":{"terms":{"field":"@fields.rspCode","size":15,"order":{"_count":"desc"}}}},"size":0,"_source":{"excludes":[]},"stored_fields":["*"],"script_fields":{},"docvalue_fields":[{"field":"@timestamp","format":"date_time"}],"query":{"bool":{"must":[{"match_phrase":{"@fields.user":{"query":"haloinv"}}},{"range":{"@timestamp":{"gte":1619071340795,"lte":1621663340795,"format":"epoch_millis"}}}],"filter":[{"match_all":{}},{"bool":{"should":[{"query_string":{"fields":["@fields.service.raw"],"query":"cts\\\\\\\\-content\\\\\\\\-*"}}],"minimum_should_match":1}}],"should":[],"must_not":[]}}}\\n{"index":"cauth","ignore_unavailable":true,"timeout":60000,"preference":1621663317737}\\n{"aggs":{"2":{"terms":{"field":"@fields.service.raw","size":50,"order":{"1":"desc"}},"aggs":{"1":{"avg":{"field":"@fields.duration"}}}}},"size":0,"_source":{"excludes":[]},"stored_fields":["*"],"script_fields":{},"docvalue_fields":[{"field":"@timestamp","format":"date_time"}],"query":{"bool":{"must":[{"match_phrase":{"@fields.user":{"query":"haloinv"}}},{"range":{"@timestamp":{"gte":1619071340795,"lte":1621663340795,"format":"epoch_millis"}}}],"filter":[{"match_all":{}},{"bool":{"filter":[{"bool":{"should":[{"query_string":{"fields":["@fields.service.raw"],"query":"cts\\\\\\\\-content\\\\\\\\-*"}}],"minimum_should_match":1}},{"bool":{"filter":[{"bool":{"must_not":{"bool":{"should":[{"match":{"@fields.beHdrXLimaUsertype":"EMPLOYEE"}}],"minimum_should_match":1}}}},{"bool":{"filter":[{"bool":{"must_not":{"bool":{"should":[{"query_string":{"fields":["@fields.beHdrXLimaUsername"],"query":"FDS_DEMO_*"}}],"minimum_should_match":1}}}},{"bool":{"must_not":{"bool":{"should":[{"match":{"@fields.serial":"FDS"}}],"minimum_should_match":1}}}}]}}]}}]}}],"should":[],"must_not":[]}}}\\n{"index":"cts_content_proxy","ignore_unavailable":true,"timeout":60000,"preference":1621663317737}\\n{"aggs":{"2":{"terms":{"field":"@fields.additionalInfo.endpoint.raw","size":27,"order":{"_count":"desc"}}}},"size":0,"version":true,"_source":{"excludes":[]},"stored_fields":["*"],"script_fields":{},"docvalue_fields":[{"field":"@timestamp","format":"date_time"}],"query":{"bool":{"must":[{"match_phrase":{"@fields.user":{"query":"haloinv"}}},{"range":{"@timestamp":{"gte":1619071340795,"lte":1621663340795,"format":"epoch_millis"}}}],"filter":[{"match_all":{}},{"match_all":{}},{"bool":{"filter":[{"bool":{"should":[{"exists":{"field":"@fields.additionalInfo.endpoint"}}],"minimum_should_match":1}},{"bool":{"must_not":{"bool":{"should":[{"bool":{"should":[{"match":{"@fields.userType":"EMPLOYEE"}}],"minimum_should_match":1}},{"bool":{"should":[{"bool":{"should":[{"match":{"@fields.userTYPE":"INTERNAL"}}],"minimum_should_match":1}},{"bool":{"should":[{"bool":{"should":[{"query_string":{"fields":["@fields.user"],"query":"FDS*"}}],"minimum_should_match":1}},{"bool":{"should":[{"bool":{"should":[{"match":{"@fields.userState":"MORPHED"}}],"minimum_should_match":1}},{"bool":{"should":[{"match":{"@fields.userType":"SYSTEM"}}],"minimum_should_match":1}}],"minimum_should_match":1}}],"minimum_should_match":1}}],"minimum_should_match":1}}],"minimum_should_match":1}}}}]}}],"should":[],"must_not":[]}},"highlight":{"pre_tags":["@kibana-highlighted-field@"],"post_tags":["@/kibana-highlighted-field@"],"fields":{"*":{}},"fragment_size":2147483647}}\\n{"index":"cts_content_proxy","ignore_unavailable":true,"timeout":60000,"preference":1621663317737}\\n{"aggs":{},"size":0,"version":true,"_source":{"excludes":[]},"stored_fields":["*"],"script_fields":{},"docvalue_fields":[{"field":"@timestamp","format":"date_time"}],"query":{"bool":{"must":[{"match_phrase":{"@fields.user":{"query":"haloinv"}}},{"range":{"@timestamp":{"gte":1619071340795,"lte":1621663340795,"format":"epoch_millis"}}}],"filter":[{"match_all":{}},{"match_all":{}},{"bool":{"filter":[{"bool":{"should":[{"exists":{"field":"@fields.additionalInfo.endpoint"}}],"minimum_should_match":1}},{"bool":{"must_not":{"bool":{"should":[{"bool":{"should":[{"match":{"@fields.userType":"EMPLOYEE"}}],"minimum_should_match":1}},{"bool":{"should":[{"bool":{"should":[{"match":{"@fields.userTYPE":"INTERNAL"}}],"minimum_should_match":1}},{"bool":{"should":[{"bool":{"should":[{"query_string":{"fields":["@fields.user"],"query":"FDS*"}}],"minimum_should_match":1}},{"bool":{"should":[{"bool":{"should":[{"match":{"@fields.userState":"MORPHED"}}],"minimum_should_match":1}},{"bool":{"should":[{"match":{"@fields.userType":"SYSTEM"}}],"minimum_should_match":1}}],"minimum_should_match":1}}],"minimum_should_match":1}}],"minimum_should_match":1}}],"minimum_should_match":1}}}}]}}],"should":[],"must_not":[]}},"highlight":{"pre_tags":["@kibana-highlighted-field@"],"post_tags":["@/kibana-highlighted-field@"],"fields":{"*":{}},"fragment_size":2147483647}}\\n{"index":"cts_content_proxy","ignore_unavailable":true,"timeout":60000,"preference":1621663317737}\\n{"aggs":{"2":{"date_histogram":{"field":"@timestamp","interval":"12h","time_zone":"Asia/Shanghai","min_doc_count":1},"aggs":{"3":{"terms":{"field":"@fields.additionalInfo.endpoint.raw","size":30,"order":{"_count":"desc"}}}}}},"size":0,"version":true,"_source":{"excludes":[]},"stored_fields":["*"],"script_fields":{},"docvalue_fields":[{"field":"@timestamp","format":"date_time"}],"query":{"bool":{"must":[{"match_phrase":{"@fields.user":{"query":"haloinv"}}},{"range":{"@timestamp":{"gte":1619071340796,"lte":1621663340796,"format":"epoch_millis"}}}],"filter":[{"match_all":{}},{"match_all":{}},{"bool":{"filter":[{"bool":{"should":[{"exists":{"field":"@fields.additionalInfo.endpoint"}}],"minimum_should_match":1}},{"bool":{"must_not":{"bool":{"should":[{"bool":{"should":[{"match":{"@fields.userType":"EMPLOYEE"}}],"minimum_should_match":1}},{"bool":{"should":[{"bool":{"should":[{"match":{"@fields.userTYPE":"INTERNAL"}}],"minimum_should_match":1}},{"bool":{"should":[{"bool":{"should":[{"query_string":{"fields":["@fields.user"],"query":"FDS*"}}],"minimum_should_match":1}},{"bool":{"should":[{"bool":{"should":[{"match":{"@fields.userState":"MORPHED"}}],"minimum_should_match":1}},{"bool":{"should":[{"match":{"@fields.userType":"SYSTEM"}}],"minimum_should_match":1}}],"minimum_should_match":1}}],"minimum_should_match":1}}],"minimum_should_match":1}}],"minimum_should_match":1}}}}]}}],"should":[],"must_not":[]}},"highlight":{"pre_tags":["@kibana-highlighted-field@"],"post_tags":["@/kibana-highlighted-field@"],"fields":{"*":{}},"fragment_size":2147483647}}\\n{"index":"cts_content_proxy","ignore_unavailable":true,"timeout":60000,"preference":1621663317737}\\n{"aggs":{"4":{"date_histogram":{"field":"@timestamp","interval":"12h","time_zone":"Asia/Shanghai","min_doc_count":1},"aggs":{"5":{"terms":{"field":"@fields.additionalInfo.endpoint.raw","size":50,"order":{"3":"desc"}},"aggs":{"3":{"avg":{"field":"@fields.duration"}}}}}}},"size":0,"version":true,"_source":{"excludes":[]},"stored_fields":["*"],"script_fields":{},"docvalue_fields":[{"field":"@timestamp","format":"date_time"}],"query":{"bool":{"must":[{"match_phrase":{"@fields.user":{"query":"haloinv"}}},{"range":{"@timestamp":{"gte":1619071340796,"lte":1621663340796,"format":"epoch_millis"}}}],"filter":[{"match_all":{}},{"match_all":{}},{"bool":{"filter":[{"bool":{"should":[{"exists":{"field":"@fields.additionalInfo.endpoint"}}],"minimum_should_match":1}},{"bool":{"must_not":{"bool":{"should":[{"bool":{"should":[{"match":{"@fields.userType":"EMPLOYEE"}}],"minimum_should_match":1}},{"bool":{"should":[{"bool":{"should":[{"match":{"@fields.userTYPE":"INTERNAL"}}],"minimum_should_match":1}},{"bool":{"should":[{"bool":{"should":[{"query_string":{"fields":["@fields.user"],"query":"FDS*"}}],"minimum_should_match":1}},{"bool":{"should":[{"bool":{"should":[{"match":{"@fields.userState":"MORPHED"}}],"minimum_should_match":1}},{"bool":{"should":[{"match":{"@fields.userType":"SYSTEM"}}],"minimum_should_match":1}}],"minimum_should_match":1}}],"minimum_should_match":1}}],"minimum_should_match":1}}],"minimum_should_match":1}}}}]}}],"should":[],"must_not":[]}},"highlight":{"pre_tags":["@kibana-highlighted-field@"],"post_tags":["@/kibana-highlighted-field@"],"fields":{"*":{}},"fragment_size":2147483647}}\\n'

response = requests.post('http://log.factset.io/search/v6/elasticsearch/_msearch', headers=headers, cookies=cookies, data=data, verify=False)


# %%


# https://www.elastic.co/guide/en/kibana/current/settings.html
# https://www.youtube.com/watch?v=mbd1YI_mzbk
# https://marcobonzanini.com/2015/02/02/how-to-query-elasticsearch-with-python/

# https://medium.com/a-layman/apm-logging-services-part-3-create-a-python-client-to-fetch-data-from-elasticsearch-532c828db784



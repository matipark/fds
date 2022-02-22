#%%

# %%
from time import sleep

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

#%%


# make chrome log requests
capabilities = DesiredCapabilities.CHROME
capabilities["loggingPrefs"] = {"performance": "ALL"}  # newer: goog:loggingPrefs
driver = webdriver.Chrome(
    desired_capabilities=capabilities, executable_path="./chromedriver"
)

# fetch a site that does xhr requests
driver.get("https://rpd.factset.io/create")
sleep(5)  # wait for the requests to take place

#%%

# extract requests from logs
logs_raw = driver.get_log("performance")
logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

def log_filter(log_):
    return (
        # is an actual response
        log_["method"] == "Network.responseReceived"
        # and json
        and "json" in log_["params"]["response"]["mimeType"]
    )

for log in filter(log_filter, logs):
    request_id = log["params"]["requestId"]
    resp_url = log["params"]["response"]["url"]
    print(f"Caught {resp_url}")
    print(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))
# %%


# https://gist.github.com/lorey/079c5e178c9c9d3c30ad87df7f70491d
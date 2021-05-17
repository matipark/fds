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


dsn = 'FDSLoader'
cxn = pyodbc.connect('DSN={dsn_name}'.format(dsn_name = dsn))




#%%


q = loadsql.get_sql_q('C:\\Github_repo\\Notes\\FDS\\xml_transcripts\\1.4.1 Retrieve All Participants from Earnings Calls in Past 3 Months.sql'
                      ,show=0,connection=dsn)

parts = pd.read_sql(q,cxn)

parts.head()




# %%

#%%

#load the clr module and use it to load the dll into memory
import clr
clr.AddReference ("Kratos_3") #note that the dll needs to be somewhere findable, such as the same folder as this file
#remember that the dll architecture (x64 or x86) must match the mode python is running in (64 bit or 32 bit)

#Now that we have loaded Kratos_3 into memory, we can start a FactSetOnDemand object
#We also need to load arrays from system in order to be able to create .NET string arrays
from System import Array
from Kratos_3 import *
from Kratos_3.Network import *
from Kratos_3.RunTimePlatform import *

def printOutFactletResults(df):
    if(df.hasError()):
        df.throwErrorIfAnyIsPresent()
    print(fsod.GetEventLogger().getOutputBuffer())
    for row in range(df.getNumberOfRows()):
        for col in range(df.getNumberOfColumns()):
            o = df.getCellAt(row, col)
            print("Row: " + str(row) + ", Col: " + str(col) + ", Value: " + str(o))

fsod = FactSetOnDemand()
config = fsod.getConfig()

# Set our configuration. We definitely need to set our username and password, as given to us by FactSet Support staff
config.setConfig(ConfigOptions.DataDirectUserName, "FDS_DEMO_FE_410734_SERVICES")
config.setConfig(ConfigOptions.DataDirectPassword, "4XJJNU4Jad6Ftf8n")



# %%

df = fsod.ExtractFormulaHistory("004561,005367,006670,008118,037537,038641,040520,040650,040828,041610,042703,044788", "FE_VALUATION(PE,MEAN,NTMA,,0M,,,\'\'),FG_GICS_SECTOR", "0M")

import numpy as np
import pandas as pd
def convertToNumpy(df):
    if(df.hasError()):
        df.throwErrorIfAnyIsPresent()
    dataset = []
    for row in range(df.getNumberOfRows()):
        lst = []
        for col in range(df.getNumberOfColumns()):
            o = df.getCellAt(row, col)
            lst.append(o)
        dataset.append(lst)
        pdf = np.array(dataset)
    return pdf

def csvToArray(n):
    data = []
    with open(n, 'r') as csvFile:
        next(csvFile)
        reader = csv.reader(csvFile)
        for row in reader:
            data.append(row[1])
    return data
    csvFile.close()

df2=convertToNumpy(df)

dataset = pd.DataFrame({'Ticker':df2[:,0],'Date':df2[:,1],'PE NTM':df2[:,2],'Sector':df2[:,3]})
print(dataset)

# %%

df = fsod.ExtractEconData('','FDS_ECON_DATA(\'HK.GDPNNSA\',0,-1AY,Q,STEP,SUM,1)') 

df2=convertToNumpy(df)

dataset = pd.DataFrame({'Ticker':df2[:,0],'Date':df2[:,1],'GDP':df2[:,2]})
print(dataset)



df = fsod.ExtractVectorFormula("PCMC", "PID(-1)");
printOutFactletResults(df); 


# %%

df = fsod.ExtractFormulaHistory("005930-kr", "P_PRICE(0,-2AY,,,,9)", "0:-2AY:D"); 
printOutFactletResults(df)


# %%
df = fsod.ExtractFormulaHistory("5386095", "P_PRICE(08/31/2017),P_PRICE_BID(08/31/2017),P_PRICE_ASK(08/31/2017)", "08/31/2017"); 
printOutFactletResults(df)
# %%

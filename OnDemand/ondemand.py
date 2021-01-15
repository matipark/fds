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

printOutFactletResults(df)


#%%

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

df2=convertToNumpy(df)

dataset = pd.DataFrame({'Ticker':df2[:,0],'Date':df2[:,1],'PE NTM':df2[:,2],'Sector':df2[:,3]})
print(dataset)


# %%

df = fsod.ExtractEconData('','FDS_ECON_DATA(\'HK.GDPNNSA\',0,-1AY,Q,STEP,SUM,1)') 

df2=convertToNumpy(df)

dataset = pd.DataFrame({'Ticker':df2[:,0],'Date':df2[:,1],'GDP':df2[:,2]})
print(dataset)

#%%



df = fsod.ExtractVectorFormula("PCMC", "PID(-1)");
printOutFactletResults(df); 


# %%

df = fsod.ExtractFormulaHistory("005930-kr", "P_PRICE(0,-2AY,,,,9)", "0:-2AY:D"); 
printOutFactletResults(df)

df2=convertToNumpy(df)

dataset = pd.DataFrame({'Ticker':df2[:,0],'Date':df2[:,1],'Price':df2[:,2]})
print(dataset)


# %%
df = fsod.ExtractFormulaHistory("5386095", "P_PRICE(08/31/2017),P_PRICE_BID(08/31/2017),P_PRICE_ASK(08/31/2017)", "08/31/2017"); 
printOutFactletResults(df)


# %%




# %%
df = fsod.ExtractFormulaHistory("xom,stl-no,fds,ibm,efc,appl,goog", "fg_eps(0,-1m,d)", "")

df2=convertToNumpy(df)

dataset = pd.DataFrame({'ticker':df2[:,0],'Date':df2[:,1],'value':df2[:,2]})
print(dataset)



#%%

##UploadToOFDB##


uFactlet = UploadFactlet("TestOFDB_Python", Array[str](["ID","Date","my_price","my_volume"]), Array[str](["Id","Date","Double","Double"]))
dates = ["04/10/2013","04/11/2013","04/12/2013"]
fds_price = [93.33, float('nan'), 92.65]
fds_volume = [388.205, float('nan'), 359.396]
xom_price = [88.68, float('nan'), 89.22]
xom_volume = [14826.0, float('nan'), 14980.0]

for i in range(len(dates)):
    uFactlet.addDataPoint('FDS')
    uFactlet.addDataPoint(dates[i])
    uFactlet.addDataPoint(fds_price[i])
    uFactlet.addDataPoint(fds_volume[i])

for i in range(len(dates)):
    uFactlet.addDataPoint('XOM')
    uFactlet.addDataPoint(dates[i])
    uFactlet.addDataPoint(xom_price[i])
    uFactlet.addDataPoint(fds_volume[i])
    
df = fsod.executeFactlet(uFactlet)
df.throwErrorIfAnyIsPresent()




# %%

# Optional arguments must go in bracket
# Directory in cap letter

data = fsod.ExtractOFDBUniverse('PERSONAL:TESTOFDB_PYTHON')
printOutFactletResults(data)

# ExtractOFDBItem
data = fsod.ExtractOFDBItem('PERSONAL:TESTOFDB_PYTHON','FDS,XOM','MY_PRICE,MY_VOLUME','')
printOutFactletResults(data)

# Screening
data=fsod.ExtractScreenUniverse('CLIENT:ASIA_QUANT_DEMO',['All','Y','includeColumns','1'])
printOutFactletResults(data)

#AT3
data = fsod.ExtractAlphaTestingSnapshot('', 'Y','CLIENT:ASIA EX JAPAN QUANT DEMO','CONSTITUENTS', 'ALL', '', '', '', '', '', '') 
printOutFactletResults(data)

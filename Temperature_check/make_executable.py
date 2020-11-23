#%%


import PyInstaller.__main__

PyInstaller.__main__.run([
    'temp_check.py',
    '--onefile',
    '--clean'
    # '--add-binary',
    # './chromedriver.exe;./'
])



# %%

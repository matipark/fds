#%%


import PyInstaller.__main__

PyInstaller.__main__.run([
    'temp_check.py',
    '--onefile',
    '--clean'
    # '--add-binary',
    # './chromedriver.exe;./'
])

# DO NOT FORGET TO CHANGE E-MAIL
# DO NOT FORGET TO REMOVE SUBMIT BUTTON IF IN TEST MODE

# %%




# https://pyinstaller.readthedocs.io/en/stable/usage.html?highlight=noconsole#options
# https://www.zacoding.com/en/post/python-selenium-to-exe/
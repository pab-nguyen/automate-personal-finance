import win32com.client
import os
import time

f = open("refresh_excel.txt", "a")
f.write(os.getcwd())
f.close()

# Connect to Excel application
excel = win32com.client.Dispatch("Excel.Application")

# Open the Excel file
file_path =  os.getcwd() + "/data/other_input/Master Ledger.xlsx "
workbook = excel.Workbooks.Open(file_path)
print('opening master ledger')
# Refresh all data connections
workbook.RefreshAll()
# excel.CalculateUntilAsyncQueriesDone()
print('finished refreshing')
time.sleep(10)


try :
    # Save and close the workbook
    workbook.save()
    print('workbook saved')
except Exception as e :  # can do better code by selecting the specific error
    pass
try :
    workbook.close()
    print('workbook closed')
except Exception as e :  # can do better code by selecting the specific error
    pass
# Quit Excel application
excel.Quit() 
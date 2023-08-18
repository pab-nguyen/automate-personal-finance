import win32com.client
import os
import time
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
# Save and close the workbook

workbook.Save()
print('workbook saved')

workbook.Close(True)
print('workbook closed')
# Quit Excel application
excel.Quit()
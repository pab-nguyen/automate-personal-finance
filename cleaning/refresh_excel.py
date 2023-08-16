import win32com.client
import os
import time
# Connect to Excel application
excel = win32com.client.Dispatch("Excel.Application")

# Open the Excel file
file_path =  os.getcwd() + "/data/other_input/Master Ledger.xlsx "
workbook = excel.Workbooks.Open(file_path)

# Refresh all data connections
workbook.RefreshAll()
excel.CalculateUntilAsyncQueriesDone()
# Save and close the workbook
workbook.Close(True)

# Quit Excel application
excel.Quit()
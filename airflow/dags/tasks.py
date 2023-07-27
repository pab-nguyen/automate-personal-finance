import subprocess
import os
def scraping():
    try:
     # Execute the external Python script using subprocess
        exec("/scraping/scraping.py")
        print("current dir"+os.getcwd())
    except Exception as e:
        print("An error occurred during script execution:", str(e))

def cleaning():
    try:
        # Execute the external Python script using subprocess
        subprocess.run(['python', "./cleaning/cleaning.py"])

    except Exception as e:
        print("An error occurred during script execution:", str(e))

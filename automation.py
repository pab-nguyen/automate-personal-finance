import subprocess
import os


# scripts_to_run = [
#     './scraping/scraping.py',
#     './sync_ggdrive/sync_ggdrive.py',
#     "./cleaning/cleaning.py",
#     "./cleaning/refresh_excel.py",
#     './sync_ggdrive/sync_ggdrive.py',
    
# ]

scripts_to_run = [
    'c:/Github Repos/automate-personal-finance/scraping/scraping.py',
    'c:/Github Repos/automate-personal-finance/sync_ggdrive/sync_ggdrive.py',
    'c:/Github Repos/automate-personal-finance/cleaning/cleaning.py',
    'c:/Github Repos/automate-personal-finance/cleaning/refresh_excel.py',
    'c:/Github Repos/automate-personal-finance/sync_ggdrive/sync_ggdrive.py',
    
]

for script in scripts_to_run:
    try:
        # Run the script using the 'python' interpreter
        subprocess.run(['C:/Github Repos/automate-personal-finance/.venv/Scripts/python.exe', script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running '{script}': {e}")
        f = open("automation_process.txt", "a")
        f.write(f"Error running '{script}': {e}")
        f.close()
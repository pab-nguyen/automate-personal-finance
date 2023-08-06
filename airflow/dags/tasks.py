import subprocess
import os


def scraping():
    exec(open("./scraping/scraping.py").read())

def cleaning():
    exec(open("./cleaning/cleaning.py").read())

def upload_to_ggdrive():
    exec(open("./upload_gg_drive/upload_to_ggdrive.py").read())

def download_from_ggdrive():
    exec(open("./upload_gg_drive/download_from_ggdrive.py").read())


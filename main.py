import requests
import shutil
import os
import concurrent 
from concurrent.futures import ThreadPoolExecutor

# Config parameters
FILE_NAME = 'wiitdb.txt'
START_FROM = 2000
THREADS = 24
URLS = ['https://art.gametdb.com/wii/coverfullHQ/US/', 'https://art.gametdb.com/wii/coverfullHQ2/US/']

coverPath = os.path.dirname(__file__) + '\\Covers'

# Creates the folder 'Covers' to download the files to
if not os.path.exists(coverPath):
    os.mkdir(coverPath)

def getCodes():
    with open(FILE_NAME, encoding="utf8") as file:
        file = file.readlines()

    modified = []
    codes = []

    # Remove the '\n' from every line
    for line in file:
        modified.append(line.strip())

    # Filter the text to only get the codes
    for line in modified:
        i = 0
        while line[i] != '=':
            i += 1

        codes.append(line[:i-1])

    # Remove the first element of the list, should be 'TITLES', comes from the file info, not used
    del codes[0]

    return codes

# We always start with zero covers downloaded (duh!)
imageCount = 0

# We set the total amount of covers available to download
# If we start from a certain point the total amount of covers to download decreases
totalCount = len(getCodes()) - START_FROM

# We start from the element we specified
codes = getCodes()[START_FROM:]

# Write the codes to a different file
with open('codes.txt', 'w') as f:
    for line in codes:
        f.write(line)
        f.write('\n')

# Main function, it uses the code for a certain game and downloads the cover from the specified URL's
# If a get from an URL fails it tries from the next one on the list and so on
# If all URL fails for a certain code it lower the total amount of covers to download
def getCover(code):
    global totalCount
    for url in URLS:
        request = requests.get(url + code + '.png', stream = True)
        if request.status_code == 200:
            directory = coverPath + '\\' + code + '.png'
            with open(directory, 'wb') as f:
                shutil.copyfileobj(request.raw, f)
            return
        
        print('Cover not Found for code: ', code)
        totalCount -= 1

# Multi-Threaded Execution of the download
with ThreadPoolExecutor(max_workers = THREADS) as executor:
    futures = [executor.submit(getCover, code) for code in codes]

    # When a task is completed we do this
    for future in concurrent.futures.as_completed(futures):
        try:
            imageCount += 1
            print('Image ', imageCount, '/', totalCount)
        except Exception as e:
            print('Looks like something went wrong:', e)

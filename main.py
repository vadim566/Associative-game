<<<<<<< HEAD
import signal
from leader_election import LeaderElection
import time

def handler(signum, frame):
    print("Ctrl-c was pressed.\nEXIT", end="", flush=True)
    exit(1)
=======
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic
>>>>>>> 02a487d8cd0fdfcc61ba6062e8613f90bd165efd

"""
#Import libraries
import os
from GoogleImageScrapper import GoogleImageScraper
from patch import webdriver_executable

<<<<<<< HEAD
if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)

    le = LeaderElection('localhost:2181', 'cmdApp', '/election')
    le.register()

    # let's make ourselves busy with some tasks
    counter = 0
    while True:
        if le.is_leader():
            #if leader
            msg = ('I am Leader\n')
            print(msg.upper())
            time.sleep(1)
        else:
            #if worker
            msg =('I am Worker - give me some text\n')
            print(msg.upper())
            #make some calculations
            counter += 1
            print('calc...' + str(counter))
            time.sleep(1)


=======
if __name__ == "__main__":
    #Define file path
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))

    #Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
    search_keys= ['Glinda, the good Sorceress of Oz, sat in the grand court of her','palace, surrounded by her maids of honor--a hundred of the most'\
                 ,'beautiful girls of the Fairyland of Oz','The palace court was built of\
rare marbles', 'exquisitely polished' ]

    #Parameters
    number_of_images = 2
    headless = False
    min_resolution=(0,0)
    max_resolution=(9999,9999)

    #Main program
    for search_key in search_keys:
        image_scrapper = GoogleImageScraper(webdriver_path,image_path,search_key,number_of_images,headless,min_resolution,max_resolution)
        image_urls = image_scrapper.find_image_urls()
        image_scrapper.save_images(image_urls)
    
    #Release resources    
    del image_scrapper
>>>>>>> 02a487d8cd0fdfcc61ba6062e8613f90bd165efd

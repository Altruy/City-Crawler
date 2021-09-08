from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import csv
import base64
import os
import sys

DRIVER_PATH = '.\chromedriver.exe'

try:
    os.mkdir('./img')
except:
    pass

t = time.time()
inFile = open('output.csv', encoding='utf-8')


def down(search_query, place, folder, name):
    place = place.split('/')[0]
    search_query = search_query.split('/')[0]
    # print('A')
    try:
        place = place.split('"')[1]
    except:
        pass
    try:
        search_query = search_query.split('"')[1]
    except:
        pass
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    try:
        browser = webdriver.Chrome(
            DRIVER_PATH, options=options)
    except:
        sys.exit(0)
    # print('B')
    search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}%2C+{place}"
    images_url = []

    # open browser and begin search
    print(place, '|', search_query)
    browser.get(search_url)
    # print('C')
    elements = browser.find_elements_by_class_name('rg_i')
    # print('D')

    e = elements[0]
    # get images source url
    e.click()
    time.sleep(1)
    # print('E')
    try:
        element = browser.find_elements_by_class_name('v4dQwb')

        images_url = element[0].find_element_by_class_name(
            'n3VNCb').get_attribute("src")
        # print('F', len(images_url))
        # write image to file
        try:
            reponse = requests.get(images_url)
            # print('G')
            if reponse.status_code == 200:
                # print('H1')
                with open(f"./img/{folder}/{name}.jpg", "wb") as file:
                    file.write(reponse.content)
        except:
            try:
                # print('H2')
                imgdata = base64.b64decode(images_url[23:])
                with open(f"./img/{folder}/{name}.jpg", 'wb') as f:
                    f.write(imgdata)
            except Exception as e:
                print('Error | '+place, '|', search_query)
                err = open('log_img.txt', mode='a', encoding='utf-8')
                err.write(str(e)+' | ' + search_query+' | ' + place+'\n')
                err.close()
                return
        # print('I')
    except Exception as e:
        print('Error || '+place, ' | ', search_query)
        err = open('log_img.txt', mode='a', encoding='utf-8')
        err.write(str(e), ' || ' + search_query + ' | ' +
                  place + ' | at seconds:' + str(time.time()-t)+'\n')
        err.close()

    browser.close()
    # print('J')


def main():
    csv_reader = csv.reader(inFile, delimiter=',')
    count = 0
    print('Images are downloading...')
    for row in csv_reader:
        place = row[1]
        folder = row[3]
        i = 0
        while i < len(row) and row[i] != 'pl1':
            i += 1
        folder = row[i-11]
        try:
            os.mkdir('./img/'+folder)
        except:
            pass
        i += 1
        while i < len(row):
            try:
                down(row[i], place, folder, row[i-1])
            except SystemExit:
                sys.exit()
            except Exception as e:
                print('Error ||| '+place, ' | ', row[i])
                err = open('log_img.txt', mode='a', encoding='utf-8')
                err.write(str(e) + ' ||| ' +
                          row[i] + ' | '+place + ' | in seconds ' + str(time.time()-t)+'\n')
                err.close()
            i += 4
        count += 1
    err = open('log_img.txt', mode='a', encoding='utf-8')
    err.write('Total places: ' + str(count) +
              '|in seconds: ' + str(time.time()-t)+'\n')
    err.close()
    inFile.close()


try:
    main()
    print('Done')
except KeyboardInterrupt:
    err = open('log_img.txt', mode='a', encoding='utf-8')
    err.write('Keyboard interrupt | ran: '+str(time.time()-t)+'\n')
    try:
        err.close()
        inFile.close()
        sys.exit(0)
    except SystemExit:
        os._exit(0)
except SystemExit:
    print('Exiting without finishing (systemexit)')
    err = open('log_img.txt', mode='a', encoding='utf-8')
    err.write('Exiting without finishing | ran: '+str(time.time()-t)+'\n')
    err.close()
    inFile.close()

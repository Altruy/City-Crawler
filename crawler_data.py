from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import sys
import os

DRIVER_PATH = '.\chromedriver.exe'

t = time.time()
fil = open('output.csv', mode='w+', encoding='utf-8')
err = open('log_data.txt', 'w+', encoding='utf-8')
inFile = open('input.csv', encoding='utf-8')


def run(line):
    try:
        place = line[1].split('/')[0]
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(DRIVER_PATH, options=options)
        try:
            driver.get('https://www.google.com/travel/things-to-do')

            driver.find_element_by_id("oA4zhb").send_keys(place)
            time.sleep(2)

            clink = driver.find_element_by_class_name('sbsb_c')
            clink.click()

            time.sleep(2)

            link = driver.current_url
            driver.get(link[:42]+'/see-all'+link[42:])

            elems = driver.find_elements_by_class_name('NnEw9')
            txt = ','.join(line) + ','
            count = 1
            for a in elems:
                txt += 'pl'+str(count)+',"'+a.find_element_by_class_name(
                    'skFvHc').text.split('/')[0] + '",'
                count += 1
                try:
                    txt += a.find_element_by_class_name(
                        'KFi5wf').text + ','
                except:
                    txt += '0.0,'
                try:
                    txt += '"' + a.find_element_by_class_name(
                        'nFoFM').text + '",'
                except:
                    txt += ','
            fil.write(txt[:-1]+'\n')
        except:
            fil.write(','.join(line)+'\n')
            err.write('exception in line: ' + ",".join(line) +
                      ' |at seconds: ' + str(time.time()-t)+'\n')
        driver.close()
    except:
        return


def main():
    csv_reader = csv.reader(inFile, delimiter=',')
    count = 0
    print('Fetching city attractions...')
    for row in csv_reader:
        run(row)
        count += 1
    err.write('Total places: ' + str(count) +
              ' |in seconds: ' + str(time.time() - t)+'\n')
    fil.close()
    err.close()
    inFile.close()


try:
    main()
    print('Done')
except KeyboardInterrupt:
    err.write('Keyboard interrupt | ran: '+str(time.time()-t)+'\n')
    try:
        fil.close()
        err.close()
        inFile.close()
        sys.exit(0)
    except SystemExit:
        os._exit(0)

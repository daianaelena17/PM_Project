from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup, NavigableString, Tag
import re
import csv
from PyQt5.uic import driver


def generate_header(fieldnames, filename):
    with open (file=filename, mode='w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=["Id"] + fieldnames)
        csv_writer.writeheader()

def take_sensors():
    URL = 'http://popescu.dyndns.org:3601/'
    
   
    while (True):
        values = []
        try:
            driver.get(URL)
            sleep(1)
            driver.find_element_by_xpath("//input[@name='bl' and @value='GET NEW DATA FROM SENSORS']").click()
            sleep(2)
            match = re.findall("<b>(.*?)<br>", driver.page_source)
            for s in match:
                s = s.replace("</b>","")
                number = [int(x) for x in s.split() if x.isdigit()]
                values.append((int (number[0])))
            if values != []:
                return values
        except:
            sleep(3)


def generate_data(fieldnames, filename, initial):
    global driver
    c_options = webdriver.ChromeOptions()
    c_options.add_argument("--headless")
    driver = webdriver.Chrome("/usr/bin/chromedriver",chrome_options=c_options)
    index = 0
    with open(file=filename, mode='a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=["Id"] + fieldnames)
        info = dict(zip(["Id"] + fieldnames, [index] + initial))
        csv_writer.writerow(info)
        data = initial
    while True:
        with open(file=filename, mode='a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=["Id"] + fieldnames)
            data = take_sensors()
            info = dict(zip(["Id"] + fieldnames, [index] + data))
            csv_writer.writerow(info)
            print(data)
            index = index + 1
        sleep(2)

def main():   
    generate_header(["value1", "value2", "value3", "value4"], "data.csv")
    generate_data(["value1", "value2", "value3", "value4"], "data.csv", [0,0,0,0])
    
if __name__ == "__main__":
    main()
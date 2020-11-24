#import relevant modules

from  selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from fractions import Fraction
from selenium.webdriver.support.ui import Select
from adjustText import adjust_text
from highlight_text.htext import htext, fig_htext

#use selenium to open FFSCOUT fixtures page
username="YOUR USERNAME"
password="YOUR PASSWORD"

driver = webdriver.Chrome(r"C:\Users\ameil\chromedriver.exe") 
url=f"https://members.fantasyfootballscout.co.uk/matches/"
driver.get(url)
driver.find_element_by_id("user_login").send_keys(f"{username}")
driver.find_element_by_id("user_pass").send_keys(f"{password}")
time.sleep(2)
driver.find_element_by_name("login").click()

#Store in a results DF
results=pd.DataFrame()
seasons=["2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"]

for season in seasons:
    
    select = Select(driver.find_element_by_id('fsid'))
    select.select_by_value(season)
    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div[1]/div[2]/div/div/form/div/input[1]").click()
    
    for i in range(1,39):
        table=f"//*[@id='content']/div/div[1]/div[2]/div/table[{i}]"
        tbl = driver.find_element_by_xpath(table).get_attribute('outerHTML')
        df_list = pd.read_html(tbl)
        df_list[0]["Gameweek"]=f"Gameweek {i}"
        df_list[0]["Season"]=season
        results=results.append(df_list[0])
        
 #functions to clean data
def get_result(x):
    return x.split("FT")[0].strip()
def get_date(x):
    return x[-14:]
def home_goals(x):
    return x[0]
def away_goals(x):
    return x[-1]
    
results["Result"]=results["Score"].apply(get_result)
results["Date"]=results["Score"].apply(get_date)
results["Home Goals"]=results["Result"].apply(home_goals)
results["Away Goals"]=results["Result"].apply(away_goals)

conditions  = [ results["Home Goals"]>results["Away Goals"], results["Home Goals"]<results["Away Goals"], 
               results["Home Goals"]==results["Away Goals"]]
choices     = [ results["Home"], results["Away"], 'Draw' ]

results["Outcome"] = np.select(conditions, choices)
results.drop("Score",inplace=True,axis=1)
results

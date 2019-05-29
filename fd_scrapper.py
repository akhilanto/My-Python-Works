''' Title: Web-scrapper for Fidelity web site.
    Execution procedure: Execute "python fd_scrapper.py" on cmd or shell for the directory in which file exists.
    Python Package requirements: Selenium=3.12.0
                                 pandas=0.23.0
                                 requests=2.18.4
                                 python=3.6.5
    Functions:
    Driver(): Creates and returns a selenium webdriver.
    get_key(): Creates a table with industries and sectors mapping.
    get_sector_data(): Web scraps sector wise data and returns a Pandas dataframe.
    get_industry_data(): Web scraps industry wise data and returns a Pandas dataframe.
    get_sector_fundamental_data(): Web scraps sector wise fundamental data and returns a Pandas dataframe.
    get_industry_fundamental_data(): Web scraps industry wise fundamental data and returns a Pandas dataframe.
    
    Note***:
    1) Adjust time.sleep(integer value) if the internet connection is slow.
    
    Requiremnts:
    [IMPORTANT] 1) Download chromedriver.exe and place it in folder "C:\chromedriver\"

    Outputs:
    1) Four CSV data files.
        - By_Sector.csv
        - By_Industry.csv
        - Fundamentals_By_sector.csv
        - Fundamentals_By_Industry.csv
'''
import pandas as pd
import requests
import time
from requests import get

def driver():
    from selenium import webdriver
    url_path = 'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml'
    chrome = webdriver.Chrome("C:\chromedriver\chromedriver.exe")
    webdriver = chrome
    webdriver.get(url_path)
    return webdriver

def get_key():
    Sector = []
    Industry = []
    webdriver= driver()
    webdriver.find_element_by_xpath('//*[@id="sector_div_container"]/table/thead/tr/th[1]/ul/li[1]/a').click()
    time.sleep(5) # Increase delay if internet slow.
    table_= webdriver.find_elements_by_xpath('//*[@id="sector_div_container"]/table/tbody/tr')
    for i in range(1,len(table_),2):
        x=webdriver.find_elements_by_xpath(f'//*[@id="sector_div_container"]/table/tbody/tr[{i}]/th/div/a')[0].text
        b=webdriver.find_elements_by_xpath(f'//*[@id="sector_div_container"]/table/tbody/tr[{i+1}]/td/div/table/tbody/tr')
        for j in range(1,1+len(b)):
            Sector.append(x)
            c= webdriver.find_elements_by_xpath(f'//*[@id="sector_div_container"]/table/tbody/tr[{i+1}]/td/div/table/tbody/tr[{j}]/th/a')[0].text
            Industry.append(c)
    return pd.DataFrame({'Sector':Sector,'Industry':Industry})

def get_sector_data():
    webdriver = driver()
    Sector =[]
    Last_Pecent_Change =[]
    Market_Cap =[]
    One_Year_Percent_Change =[]
    As_of_Date_Time=[]
    count = webdriver.find_elements_by_xpath('//*[@id="sector_div_container"]/table/tbody/tr')
    for i in range(1,len(count)):
        a=webdriver.find_elements_by_xpath(f'//*[@id="sector_div_container"]/table/tbody/tr[{i}]/th/div/a')[0].text
        Sector.append(a)
        b=webdriver.find_elements_by_xpath(f'//*[@id="sector_div_container"]/table/tbody/tr[{i}]/td[1]')[0].text
        Last_Pecent_Change.append(b)
        c=webdriver.find_elements_by_xpath(f'//*[@id="sector_div_container"]/table/tbody/tr[{i}]/td[2]')[0].text
        Market_Cap.append(c)
        d=webdriver.find_elements_by_xpath(f'//*[@id="sector_div_container"]/table/tbody/tr[{i}]/td[3]/span[2]')[0].text
        One_Year_Percent_Change.append(d)
        e=webdriver.find_elements_by_xpath('//*[@id="sector_div_container"]/table/thead/tr/th[2]/span/time')[0].text
        As_of_Date_Time.append(e)
    return pd.DataFrame({'Sector':Sector,'Last_Pecent_Change ':Last_Pecent_Change,'Market_Cap':Market_Cap,'One_Year_Percent_Change ':One_Year_Percent_Change ,'As_of_Date_Time':As_of_Date_Time})

def get_industry_data():
    webdriver= driver()
    webdriver.find_element_by_xpath('//*[@id="tab_industry"]').click()
    time.sleep(5) # Increase delay if internet slow.
    t1 = webdriver.find_elements_by_xpath('//*[@id="tableSort"]/thead/tr/th[2]/span/time')[0].text # table header.
    trs=webdriver.find_elements_by_xpath('//*[@id="tableSort"]/tbody/tr') # table body rows.
    Industry =[]
    Last_Pecent_Change =[]
    Market_Cap =[]
    One_Year_Percent_Change =[]
    As_of_Date_Time=[]
    for i in range(len(trs)):
        a=trs[i].find_elements_by_tag_name('th')[0].text
        Industry.append(a)
        b=trs[i].find_elements_by_tag_name('td')[0].text
        Last_Pecent_Change.append(b)
        c= trs[i].find_elements_by_tag_name('td')[1].text
        Market_Cap.append(c)
        d=trs[i].find_elements_by_tag_name('td')[2].text
        One_Year_Percent_Change.append(d)
        t1 = webdriver.find_elements_by_xpath('//*[@id="tableSort"]/thead/tr/th[2]/span/time')[0].text
        As_of_Date_Time.append(t1)
    return pd.DataFrame({'Industry':Industry,'Last_Pecent_Change ':Last_Pecent_Change,'Market_Cap':Market_Cap,'One_Year_Percent_Change ':One_Year_Percent_Change ,'As_of_Date_Time':As_of_Date_Time})

def get_sector_fundamental_data():
    webdriver= driver()
    body = webdriver.find_elements_by_xpath('//*[@id="sector_div_container"]/table/tbody/tr')
    sector =[]
    Fundamentals=[]
    value =[]
    As_of_Date=[]
    for j in range(1,1+len(body)):
        time.sleep(2) # Increase delay if internet slow.
        s=webdriver.find_elements_by_xpath(f'//*[@id="sector_div_container"]/table/tbody/tr[{j}]/th/div/a')[0].text
        webdriver.find_element_by_xpath(f'//*[@id="sector_div_container"]/table/tbody/tr[{j}]/th/div/a').click()
        count = webdriver.find_elements_by_xpath('//*[@id="contentContainer"]/div[2]/div[5]/div[1]/section[2]/div[1]/table/tbody/tr')
        time.sleep(8) # Increase delay if internet slow.
        for i in range(1,len(count)):
            sector.append(s)
            I=webdriver.find_elements_by_xpath(f'//*[@id="contentContainer"]/div[2]/div[5]/div[1]/section[2]/div[1]/table/tbody/tr[{i}]/th/a')[0].text
            Fundamentals.append(I)
            Id =webdriver.find_elements_by_xpath(f'//*[@id="contentContainer"]/div[2]/div[5]/div[1]/section[2]/div[1]/table/tbody/tr[{i}]/td')[0].text
            value.append(Id)
            f=webdriver.find_elements_by_xpath('//*[@id="contentContainer"]/div[2]/div[5]/div[1]/section[2]/div[1]/h2/span')[0].text
            As_of_Date.append(f)
        webdriver.execute_script("window.history.go(-1)")
    return pd.DataFrame({'sector':sector,'Fundamentals ':Fundamentals,'value':value,'As_of_Date':As_of_Date})

def get_industry_fundamental_data():
    webdriver= driver()
    webdriver.find_element_by_xpath('//*[@id="tab_industry"]').click()
    time.sleep(8) # Increase delay if internet slow.
    trs=webdriver.find_elements_by_xpath('//*[@id="tableSort"]/tbody/tr')
    Industry = []
    Fundamentals=[]
    value =[]
    As_of_Date=[]
    for j in range(1,len(trs)):
        time.sleep(8) # Increase delay if internet slow.
        webdriver.find_element_by_xpath('//*[@id="tab_industry"]').click()
        time.sleep(8) # Increase delay if internet slow.
        webdriver.find_element_by_xpath('//*[@id="tableSort"]/thead/tr/th[1]/a').click()
        time.sleep(5)
        a=webdriver.find_elements_by_xpath(f'//*[@id="tableSort"]/tbody/tr[{j}]/th/a')[0].text
        webdriver.find_element_by_xpath(f'//*[@id="tableSort"]/tbody/tr[{j}]/th/a').click()
        count = webdriver.find_elements_by_xpath('//*[@id="contentContainer"]/div[2]/div[5]/div[1]/section[2]/div[1]/table/tbody/tr')
        time.sleep(3) # Increase delay if internet slow.
        for i in range(1,len(count)):
                Industry.append(a)
                I=webdriver.find_elements_by_xpath(f'//*[@id="contentContainer"]/div[2]/div[5]/div[1]/section[2]/div[1]/table/tbody/tr[{i}]/th/a')[0].text
                Fundamentals.append(I)
                Id =webdriver.find_elements_by_xpath(f'//*[@id="contentContainer"]/div[2]/div[5]/div[1]/section[2]/div[1]/table/tbody/tr[{i}]/td')[0].text
                value.append(Id)
                f=webdriver.find_elements_by_xpath('//*[@id="contentContainer"]/div[2]/div[5]/div[1]/section[2]/div[1]/h2/span')[0].text
                As_of_Date.append(f)
        webdriver.execute_script("window.history.go(-1)")
    return pd.DataFrame({'Industry':Industry,'Fundamentals':Fundamentals,'value':value,'As_of_Date':As_of_Date}).drop_duplicates()

if __name__ == '__main__':
    #STEP-1: Key Generator (Generates sector and industry information.)
    key = get_key()

    #STEP-2: Get Sector information (Gets sector infromation from the webpage.)
    sector_data = get_sector_data()
    sector_data['As_of_Date_Time']=sector_data['As_of_Date_Time'].apply(lambda x : ' '.join(x.split()[2:]))
    sector_data.to_csv("By_Sector.csv") # Save sector data to csv.

    #STEP-3: Get Industry information (Gets Industry infromation from the webpage.)
    industry_data = get_industry_data()
    industry_data['As_of_Date_Time']=industry_data['As_of_Date_Time'].apply(lambda x : ' '.join(x.split()[2:]))
    industry_data=industry_data.set_index('Industry')
    key_ =key
    key_=key_.set_index('Industry')
    sectored_industry_data = industry_data.join(key_)
    sectored_industry_data = sectored_industry_data.reset_index(drop=False)
    sectored_industry_data.to_csv('By_Industry.csv')

    #STEP-4: Get Fundamentals by Sector information (Gets Fundamentals by Sector infromation from the webpage.)
    sector_fundamental_data = get_sector_fundamental_data()
    sector_fundamental_data['As_of_Date']=sector_fundamental_data['As_of_Date'].apply(lambda x : x.split()[2])
    sector_fundamental_data = sector_fundamental_data.pivot_table(index=['sector','As_of_Date'],columns=['Fundamentals '], values='value',aggfunc=lambda x: ''.join(x))
    sector_fundamental_data.to_csv('Fundamentals_By_sector.csv')
 
    #STEP-5: Get Fundamentals by Industry information (Gets Fundamentals by Industry infromation from the webpage.)
    industry_fundamental_data = get_industry_fundamental_data()
    industry_fundamental_data['As_of_Date']=industry_fundamental_data['As_of_Date'].apply(lambda x : x.split()[2])
    industry_fundamental_data = industry_fundamental_data.pivot_table(index=['Industry','As_of_Date'],columns=['Fundamentals'], values='value',aggfunc=lambda x: ''.join(x))
    industry_fundamental_data = industry_fundamental_data.reset_index()
    industry_fundamental_data = pd.merge(left=industry_fundamental_data,right=key, left_on='Industry', right_on='Industry')
    cols = industry_fundamental_data.columns.tolist()
    industry_fundamental_data =industry_fundamental_data[cols[-1:] + cols[:-1]]
    # Write fundamental by industry
    industry_fundamental_data.to_csv('Fundamentals_By_Industry.csv')

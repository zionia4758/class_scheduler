import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup as bs

import json
from io import StringIO
import time

def selectGrage(driver,_grade):
    grade=driver.find_element_by_name('strIsuGrade')
    select=Select(grade)
    select.select_by_visible_text(_grade)

def selectSemester(driver,_semester):
    semester=driver.find_element_by_name('strSuupTerm')
    select=Select(semester)
    select.select_by_visible_text(_semester)
    
def setMajor(driver):
    majorclass=driver.find_element_by_xpath('//*[@id="hak"]')
    majorclass.click()
    getCollegeList(driver)

def setLiberalArt(driver):
    majorclass=driver.find_element_by_xpath('//*[@id="gong"]')
    majorclass.click()
    getAreaList(driver)


def getAreaList(driver):

    

    time.sleep(1)
    soup=bs(driver.page_source,'html.parser')
    table=soup.select('#cbYungyuk>option')
    print(table)
    for college in table:
        print(college.string)
        #단과선택
        major=driver.find_element_by_xpath('//*[@id="cbYungyuk"]')
        select=Select(major)
        select.select_by_visible_text(college.string)
        
        majorCrowling(driver,college.string)
   


def getCollegeList(driver):


    time.sleep(1)
    soup=bs(driver.page_source,'html.parser')
    table=soup.select('#cbDaehak>option')
    for college in table:
        print(college.string)
        selectCollege(driver,college.string)
   



def selectCollege(driver,_college):
    print(_college)
    majorclass=driver.find_element_by_xpath('//*[@id="hak"]')
    majorclass.click()
    college=driver.find_element_by_xpath('//*[@id="cbDaehak"]')
    select=Select(college)
    select.select_by_visible_text(_college)

    time.sleep(1)
    soup=bs(driver.page_source,'html.parser')
    majors=soup.find('select',id='cbHakgwajungong')
  #  print(majors)

    majorList=majors.find_all('option')
   # print(majorList[0].string)
    for i in majorList:
        print(i.string)
        #단과선택
        major=driver.find_element_by_xpath('//*[@id="cbHakgwajungong"]')
        select=Select(major)
        select.select_by_visible_text(i.string)
        
        majorCrowling(driver,i.string)


def majorCrowling(driver, _major):

#조회버튼
    tab=driver.find_element_by_xpath('//*[@id="btn_Find"]')
    tab.click()

    

#tab개수만큼 크롤링
    soup=bs(driver.page_source,'html.parser')
    lastPage=soup.find('tfoot')
    lastPage=lastPage.find_all('a')
    if(len(lastPage)>1):
        lastPage=lastPage[-1]
        lastPageStr=lastPage['onclick']
        pageNum=int(lastPageStr[lastPageStr.find('(')+1:lastPageStr.find(')')])
    elif(len(lastPage)==0):
        return
    else:
        pageNum=1
    print(pageNum)

    jsonData={}
    jsonData['major']=_major
    jsonData['classList']=[]

    for j in range(1,pageNum+1):
        next="ServiceController.goPage("+str(j)+")"
        print("page"+str(j))

        driver.execute_script(next)
        soup=bs(driver.page_source,'html.parser')
        area=soup.find('table',id='gdMain')
        #print(area)
        area=area.find('tbody')
        table=area.find_all('tr')
        #print(table)
        for i in range(0,len(table)):
            line=table[i]
            attr=line.find_all('td')

            grade=attr[0].string
            classTag=attr[1].string
            area=attr[4].string
            classNum=attr[5].string
            className=attr[8].string
            professor=attr[12].string
            credit=attr[13].string
            classTime=attr[19].get_text()
            classRoom=attr[20].string
            data={'학년':grade,'반':classTag,'영역':area, '수업번호':classNum,
                  '교과목명':className,'교강사':professor,'학점':credit,'수업시간':classTime,
                  '강의실':classRoom}
            jsonData['classList'].append(json.dumps(data,ensure_ascii=False,indent=4))
            #print(data)
            #print(json.dumps(data,ensure_ascii=False))
            #print(json.loads(json.dumps(data)))
            #print(data)
    filename=_major+'.json'
    file=open(filename,'w',encoding='utf-8')
    json.dump(jsonData,file,ensure_ascii=False,indent=4)
    file.close()

        
def main():

    URL="https://portal.hanyang.ac.kr/sugang/sulg.do"

    driver=webdriver.Chrome(executable_path='chromedriver')
    driver.get(url=URL)

    driver.implicitly_wait(time_to_wait=5)


    #수강편람
  #  print(len(driver.window_handles))
    tab=driver.find_element_by_link_text("수강편람")
    #print(tab)
    tab.click()

   # selectGrade(driver,'3학년')
    selectSemester(driver,"2학기")

    setLiberalArt(driver)
    
    setMajor(driver)


#    driver.close()


if __name__=='__main__':
    main()

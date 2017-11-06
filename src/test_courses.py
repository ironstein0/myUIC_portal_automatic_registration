from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from send_sms import send_sms
import threading

# CONSTANTS
USER_NAME = "rkaran3@uic.edu"
USER_PASSWORD = "AlbertEinstein011235"
TERM = "220181"
INTERESTED_COURSE_NUMBERS = ['501', '583', '511', '489']

def get_chrome_driver(incognito=False):
    # options for the webdriver
    chrome_options = webdriver.ChromeOptions()
    if incognito:
        chrome_options.add_argument("--incognito")

    # instantiate webdriver
    return webdriver.Chrome(chrome_options=chrome_options)

def find_element_by_href(driver, href): 
    return driver.find_element_by_xpath('//a[@href="' + href + '"]')

driver = get_chrome_driver(incognito=True)
driver.get("https://my.uic.edu/uPortal")

# my.uic.edu
# login_link = find_element_by_href(driver, 'https://my.uic.edu/uPortal')
# login_link.click()

# my.uic.edu/uPortal
user_id_field = driver.find_element_by_xpath('//input[@id="UserID"]')
user_id_field.send_keys(USER_NAME)
password_field = driver.find_element_by_xpath('//input[@id="password"]')
password_field.send_keys(USER_PASSWORD)
login_button = driver.find_element_by_xpath('//button[@class="btn btn-lg btn-primary btn-block"]')
login_button.click()

# https://my.uic.edu/uPortal/render.userLayoutRootNode.uP;jsessionid=28394081EB8B9D77AE5D9779CD1A2558
academics_tab = find_element_by_href(driver, 'render.userLayoutRootNode.uP?uP_root=root&uP_sparam=activeTabTag&activeTabTag=Academics&uP_sparam%3DprevTabTag%26prevTabTag%3DMy+Home&uP_sparam=showSitemap&showSitemap=no')
academics_tab.click()
student_self_service_login = find_element_by_href(driver, 'https://my.uic.edu/uPortal/b2euic03?redirect=https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin&redirectParam=appName=edu.uillinois.aits.SelfServiceLogin&redirectParam=dad=BANPROD2&redirectParam=target=A')
student_self_service_login.click()

driver.switch_to_window(driver.window_handles[1])
time.sleep(5)

lookup_classes_link = driver.find_element_by_link_text('Look-up or Select Classes')
lookup_classes_link.click()
i_agree_link = driver.find_element_by_link_text('I Agree to the Above Statement')
i_agree_link.click()

select_term = driver.find_element_by_id('term_input_id')
select_term.click()
all_options = select_term.find_elements_by_tag_name('option')
for option in all_options:
    if option.get_attribute('value') == TERM:
        option.click()
        select_term.click()
        select_term.submit()
        break

select_course = driver.find_element_by_xpath('//table[@class="dataentrytable"]')
all_options = select_course.find_elements_by_tag_name('option')
for option in all_options:
    if option.get_attribute('value') == 'CS':
        option.click()
        break

course_search_button = driver.find_element_by_xpath('//input[@value="Course Search"]')
course_search_button.click()

courses_table = driver.find_element_by_xpath('//table[@summary="This layout table is used to present the course found"]')
courses = courses_table.find_element_by_xpath('//tbody').find_elements_by_xpath('//tr')

course_availability_status_dictionary = {}

def monitor_course(course_form_link_element, course_number, course_name):
    print('monitoring course number : ' + course_number)
    course_form_link_element.find_elements_by_tag_name('input')[-1].click()
    courses_description_table = driver.find_element_by_xpath('//table[@summary="This layout table is used to present the sections found"]')
    course_options = courses_description_table.find_elements_by_tag_name('tbody')
    course_options = course_options[0].find_elements_by_tag_name('tr')
    is_available = False
    for course in  course_options:
        try:
            checkboxes = course.find_elements_by_tag_name('td')[0].find_elements_by_tag_name('input')
            if len(checkboxes) > 0:
                is_available = True
                break
        except:
            pass
    driver.back()

    def send_sms_():
        send_sms('course number : ' + course_number + '\ncourse name : ' + course_name + '\nis available : ' + str(is_available))

    # if course_number not in course_availability_status_dictionary.keys():
    #     # no previous records
    #     course_availability_status_dictionary[course_number] = is_available
    #     if is_available:
    #         # course available
    #         send_sms_()
    # else:
    #     # yes previous records
    #     if course_availability_status_dictionary[course_number] != is_available:
    #         course_availability_status_dictionary[course_number] = is_available
    #         send_sms_()

    send_sms_()

def monitor_all_courses(driver):
    courses_table = driver.find_element_by_xpath('//table[@summary="This layout table is used to present the course found"]')
    courses = courses_table.find_element_by_xpath('//tbody').find_elements_by_xpath('//tr')
    i = 0
    for i in range(len(courses)):
        course = courses[i]
        course_number = None
        course_name = None
        course_form_link = None
        try:
            course_number, course_name, course_form_link = [element.text for element in course.find_elements_by_tag_name('td')]
        except Exception as e:
            continue
    
        course_form_link = course.find_elements_by_tag_name('td')[-1]
        if course_number in INTERESTED_COURSE_NUMBERS:
            monitor_course(course_form_link, course_number, course_name)
            courses_table = driver.find_element_by_xpath('//table[@summary="This layout table is used to present the course found"]')
            courses = courses_table.find_element_by_xpath('//tbody').find_elements_by_xpath('//tr')

    print(course_availability_status_dictionary)

while True:
    monitor_all_courses(driver)
    time.sleep(15)
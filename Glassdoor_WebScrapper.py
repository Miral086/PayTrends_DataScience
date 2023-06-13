# -*- coding: utf-8 -*-
"""
Created on Tue May 30 10:15:37 2023

@author: miral
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

def get_jobs(keyword, location, num_jobs, verbose, path, sleep_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)
    url = "https://www.glassdoor.co.in/Job/{location}-{keyword}-jobs-SRCH_IL.0,5_IN115_KO6,20.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&typedLocation={location}&context=Jobs&dropdown=0".format(keyword=keyword, location=location)
    driver.get(url)
    jobs = []
    
    
    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(4)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(0.1)

        try:
            driver.find_element_by_css_selector('[alt="Close"]').click()  #clicking to the X.
            #print('x out passed')
        except NoSuchElementException:
            #print("x out failed")
            pass
    
        #job_cards = driver.find_elements_by_class_name("jobCard")
        #href_list = []
        #for job_card in job_cards:
         #   href = job_card.get_attribute("href")
          #  href_list.append(href)
            



        #Going through each job in this page
        job_buttons = driver.find_elements_by_css_selector('a[data-test="job-link"]') #jl for Job Listing. These are the buttons we're going to click.
        print(len(job_buttons))
        
        
    
        for job_button in job_buttons:  
            
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
            actions = ActionChains(driver)
            actions.move_to_element(job_button).click().perform()
            job_button.click()  #You might
            #print("done1")
            time.sleep(1)
            # try:
            #     retry = driver.find_element_by_css_selector('#JDCol > div > div.css-17bh0pp.erj00if0 > button')
            #     retry.click()
            # except:
            #     pass
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_css_selector('div[data-test="employerName"]').text
                    location = driver.find_element_by_css_selector('div[data-test="location"]').text
                    job_title = driver.find_element_by_css_selector('div[data-test="jobTitle"]').text
                    
                    #job_description = job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    job_description_element = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]')
                    # Get the inner HTML of the element
                    job_description_html = job_description_element.get_attribute('innerHTML')
                    # Process the HTML to extract the text
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(job_description_html, 'html.parser')
                    job_description = soup.get_text(separator='\n')

                    collected_successfully = True
                    
                except:
                    time.sleep(5)
                    #print("doneexcept")
                
                try:
                    salary_estimate = driver.find_element_by_css_selector('span[data-test="detailSalary"]').text
                except NoSuchElementException:
                    salary_estimate = -1 #You need to set a "not found value. It's important."
                
                try:
                    rating = driver.find_element_by_css_selector('span[data-test="detailRating"]').text
                except NoSuchElementException:
                    rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                #parent_div = driver.find_element_by_id('CompanyContainer').click()
                parent_div = driver.find_element_by_css_selector('div.d-flex.flex-wrap')
                try:
                    #<div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    #</div>
                    headquarters = parent_div.find_element_by_xpath('//span[text()="Headquarters"]/following-sibling::span').text
                except NoSuchElementException:
                    headquarters = -1

                try:
                    size = parent_div.find_element_by_xpath('//span[text()="Size"]/following-sibling::span').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = parent_div.find_element_by_xpath('//span[text()="Founded"]/following-sibling::span').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = parent_div.find_element_by_xpath('//span[text()="Type"]/following-sibling::span').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = parent_div.find_element_by_xpath('//span[text()="Industry"]/following-sibling::span').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = parent_div.find_element_by_xpath('//span[text()="Sector"]/following-sibling::span').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = parent_div.find_element_by_xpath('//span[text()="Revenue"]/following-sibling::span').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = parent_div.find_element_by_xpath('//span[text()="Competitiors"]/following-sibling::span').text
                except NoSuchElementException:
                    competitors = -1

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1

                
            if verbose:
                print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Headquarters" : headquarters,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,
            "Competitors" : competitors})
            #add job to jobs
            
        #Clicking on the "next page" button
        try:
            button = driver.find_element_by_class_name('nextButton').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    driver.quit()
    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
# Pay Trends In DataScience
![Alt Text](https://github.com/Miral086/PayTrends_DataScience/blob/main/Paytrends_web.gif)
* Developed a data science salary estimation tool with a Mean Absolute Error (MAE) of approximately &#8377;20K, aimed at aiding data scientists in income negotiation during job acquisition.
* Utilized Python and Selenium to scrape a dataset of over 1000 job descriptions from Glassdoor, ensuring a comprehensive and diverse data collection.
* Conducted feature engineering on the text of each job description to quantify the significance attributed by companies to skills such as Python, Excel, AWS, and Spark.
* Employed GridsearchCV to optimize Linear, Lasso, and Random Forest Regressors, enabling the identification of the best-performing model.
* Implemented a client-facing API using Flask, allowing seamless access and utilization of the salary estimation tool.

# Code and Resources Used
Python Version: 3.7
Packages: pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, json, pickle
For Web Framework Requirements: pip install -r requirements.txt
Flask Productionization: https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2

# Web Scraping
Tweaked the web scraper github repo (above) to scrape 1000 job postings from glassdoor.com. With each job, we got the following:

* Job title
* Salary Estimate
* Job Description
* Rating
* Company
* Location
* Company Size
* Company Founded Date
* Type of Ownership
* Industry
* Sector
* Revenue

# Data Cleaning
After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:

* Parsed numeric data out of salary
* Made columns for employer provided salary and hourly wages
* Removed rows without salary
* Parsed rating out of company text
* Made a new column for company state
* Added a column for if the job was at the company’s headquarters
* Transformed founded date into age of company
* Made columns for if different skills were listed in the job description:
  * Python
  * R
  * Excel
  * AWS
  * Spark
  * Column for simplified job title and Seniority
  * Column for description length

# EDA
I looked at the distributions of the data and the value counts for the various categorical variables. Below are a few highlights from the pivot tables.

![Salary By Job Title](https://github.com/Miral086/PayTrends_DataScience/blob/main/salary_by_job_title.png)
![Positions By City](https://github.com/Miral086/PayTrends_DataScience/blob/main/positions_by_city.png)
![Correlation Visual](https://github.com/Miral086/PayTrends_DataScience/blob/main/correlation_visual.png)

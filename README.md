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

# Data Visualization
I have created an interactive and visually appealing data visualization dashboard using Power BI. The attached GIF showcases the dynamic charts, graphs, and insights derived from the data, providing a comprehensive overview of the information at a glance.

![Alt Text](https://github.com/Miral086/PayTrends_DataScience/blob/main/Dashboard.gif)


# Model Building
First, I transformed the categorical variables into dummy variables. I also split the data into train and tests sets with a test size of 20%.

I tried three different models and evaluated them using Mean Absolute Error. I chose MAE because it is relatively easy to interpret and outliers aren’t particularly bad in for this type of model.

I tried three different models:

Multiple Linear Regression – Baseline for the model
Lasso Regression – Because of the sparse data from the many categorical variables, I thought a normalized regression like lasso would be effective.
Random Forest – Again, with the sparsity associated with the data, I thought that this would be a good fit.

# Model performance
The Random Forest model far outperformed the other approaches on the test and validation sets.

### * Random Forest : MAE = 2.32
### * Lasso Regression: MAE = 2.27
### * Linear Regression : MAE = 2.50

# Productionization
I have developed a Flask application deployed on the localhost, which automates the process of fetching details from a dataset containing information for 851 companies. Leveraging this data, the application enables users to input a job description, and based on it, predicts the salary, providing valuable insights into potential earnings for specific roles in the field.

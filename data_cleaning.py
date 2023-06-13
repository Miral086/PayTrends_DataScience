# -*- coding: utf-8 -*-
"""
Created on Wed May 31 10:44:01 2023

@author: miral
"""

import pandas as pd
import matplotlib.pyplot as plt
import nltk
# nltk.download()
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords
import string
nltk.download('punkt')
nltk.download('stopwords')

df = pd.read_csv("D:\ResumeThings\PayTrends_DataScience\csv\glassdoor_data.csv")

#removing duplicates
df = df.drop_duplicates()
df = df.drop('Headquarters', axis=1)
df = df.drop('Competitors', axis=1)

#salary parsing

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0)

df = df[df['Salary Estimate'] != '-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])

minus_LR = salary.apply(lambda x: x.replace('L','').replace("₹", ''))
min_hr = minus_LR.apply(lambda x: x.replace('Per hour','').replace('Employer Provided Salary', '').replace(':','').replace('T', '000').replace(',',''))
min_hr = min_hr.apply(lambda x: x.split('.')[0])

df['min_salary'] = min_hr.apply(lambda x: x if ':' in x else int(x.split('-')[0]))
df['max_salary'] = min_hr.apply(lambda x: x if '-' not in x else int(x.split('-')[1]))

df['max_salary'] = df['max_salary'].astype('int64')
print(df['max_salary'].dtype)

df['min_salary'] = df['min_salary'].apply(lambda x: (x*12)/100000 if x>1000 else x)
df['max_salary'] = df['max_salary'].apply(lambda x: (x*12)/100000 if x>1000 else x)

df['avg_salary'] = (df['min_salary'] + df['max_salary'])/2
    
#company name text only
df['Company'] = df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3], axis = 1)

#location
df.Location.value_counts()

#age of company
df['Company_age'] = df['Founded'].apply(lambda x: x if x<1 else 2023-x) 

#parsing of job description

df['Job Description'] = df['Job Description'].str.replace('[^\w\s]', '')
df['Job Description'] = df['Job Description'].str.replace('\d+', '')
df['Job Description'] = df['Job Description'].str.strip().str.lower()

def remove_stopwords_punctuation(text):
    # Tokenize the text into individual words
    tokens = nltk.word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    # Remove punctuation
    filtered_tokens = [word for word in filtered_tokens if word not in string.punctuation]
    
    # Join the filtered tokens back into a single string
    cleaned_text = ' '.join(filtered_tokens)
    
    return cleaned_text

text = ' '.join(df['Job Description'])
print(text)
text = remove_stopwords_punctuation(text)

print(text)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Create a figure and axes
fig, ax = plt.subplots(figsize=(10, 5))

# Display the word cloud image
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')

# Show the plot
plt.show()

word_list = ['Python','R Studio','R-Studio',
    'SQL','Java',
    'Data Manipulation',
    'Analysis',
    'Visualization',
    'machine', 'learning'
    'Statistical','Analysis',
    'Big','Data',
    'Apache','Hadoop',
    'Spark',
    'Distributed Computing',
    'Database',
    'SQL',
    'NoSQL',
    'Web',
    'HTML',
    'CSS',
    'JavaScript',
    'Django',
    'Flask',
    'Data Engineering',
    'Pipelines',
    'ETL',
    'Database Design',
    'Cloud',
    'AWS',
    'Microsoft','Azure',
    'Google',
    'Security',
    'Privacy',
    'Anonymization',
    'Communication',
    'mlops', 'visualization', 'visualisation'
]

word_list = [word.lower() for word in word_list]
def filter_words(text, word_list):
    words = text.split()
    filtered_words = [word for word in words if word in word_list]
    filtered_text = ' '.join(filtered_words)
    return filtered_text

skills = filter_words(text, word_list)
print(skills)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(skills)

# Create a figure and axes
fig, ax = plt.subplots(figsize=(10, 5))

# Display the word cloud image
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')

# Show the plot
plt.show()

df['python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['R'] = df['Job Description'].apply(lambda x: 1 if 'R' in x.lower() or 'r-studio' in x.lower() else 0)
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df['visualization'] = df['Job Description'].apply(lambda x: 1 if 'visualization' in x.lower() else 0)
df['ml'] = df['Job Description'].apply(lambda x: 1 if 'machine' in x.lower() and 'learning' in x.lower() else 0)
df['database'] = df['Job Description'].apply(lambda x: 1 if 'database' in x.lower() else 0)
df['pipelines'] = df['Job Description'].apply(lambda x: 1 if 'pipelines' in x.lower() else 0)
df['cloud'] = df['Job Description'].apply(lambda x: 1 if 'cloud' in x.lower() else 0)
df['security'] = df['Job Description'].apply(lambda x: 1 if 'security' in x.lower() else 0)
df['sql'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)
df['etl'] = df['Job Description'].apply(lambda x: 1 if 'etl' in x.lower() else 0)
df['html'] = df['Job Description'].apply(lambda x: 1 if 'html' in x.lower() else 0)
df['nosql'] = df['Job Description'].apply(lambda x: 1 if 'nosql' in x.lower() else 0)
df['javasript'] = df['Job Description'].apply(lambda x: 1 if 'javasript' in x.lower() else 0)
df['css'] = df['Job Description'].apply(lambda x: 1 if 'css' in x.lower() else 0)
df['azure'] = df['Job Description'].apply(lambda x: 1 if 'azure' in x.lower() else 0)
df['hadoop'] = df['Job Description'].apply(lambda x: 1 if 'hadoop' in x.lower() else 0)
df['mlops'] = df['Job Description'].apply(lambda x: 1 if 'mlops' in x.lower() else 0)
df['flask'] = df['Job Description'].apply(lambda x: 1 if 'flask' in x.lower() else 0)
df['django'] = df['Job Description'].apply(lambda x: 1 if 'django' in x.lower() else 0)
df['apache'] = df['Job Description'].apply(lambda x: 1 if 'apache' in x.lower() else 0)
df['data_mining'] = df['Job Description'].apply(lambda x: 1 if 'data' in x.lower() and 'mining' in x.lower() else 0)
print("hello")
df.to_csv('D:\ResumeThings\PayTrends_DataScience\cleaned.csv', index = False)

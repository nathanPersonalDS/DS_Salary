# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 00:03:08 2022

@author: lazar
"""

import pandas as pd

df= pd.read_csv('glassdoor_jobs.csv')

#salary parsing
#get company name text only
#state field
#age of company
#parsing of job description


#SALARY PARSING
#check if contains
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if'employer provided salary' in x.lower() else 0)


#remove -1
df = df[df['Salary Estimate'] !='-1']

# remove (glasdoor) text
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])

#remove K and $
minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$',''))

#remove text
min_hr = minus_Kd.apply(lambda x: x.lower().replace('per hour', '').replace('employer provided salary','').replace(':',''))

#get minimum, maximum and avg salary
df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))
df['avg_salary']= (df.min_salary + df.max_salary)/2


#COMPANY NAME 
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3], axis =1)

#STATE FIELD 
df['job_state']= df['Location'].apply(lambda x: x.split(',')[1])
df.job_state.value_counts()

df['same_state']= df.apply(lambda x:1 if x.Location == x.Headquarters else 0, axis =1)

#AGE OF COMPANY
df['age'] = df.Founded.apply(lambda x: x if x <1 else 2022 -x)


#JOB Desc(python, etc.)

#python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower()else 0)
df.python_yn.value_counts()
#r studio
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'rstudio' in x.lower() or 'r-studio' in x.lower() else 0)
df.R_yn.value_counts()
#spark
df['spark_yn'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower()else 0)
df.spark_yn.value_counts()
#aws
df['aws_yn'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower()else 0)
df.aws_yn.value_counts()
#excel
df['excel_yn'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower()else 0)
df.excel_yn.value_counts()

#drop unnamed column
df.columns

df_out = df.drop(['Unnamed: 0'], axis =1)

df_out.to_csv('salary_data_cleaned.csv', index = False)

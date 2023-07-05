# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 12:23:17 2023

@author: Admin
"""

import pandas as pd
import numpy as np
import datetime

df = pd.read_csv("glassdoor_jobs.csv")

# Salary Estimate cleanup
df["Hourly"] = df["Salary Estimate"].apply(
    lambda x: 1 if 'per hour' in x.lower() else 0)
df["Employer Provided"] = df["Salary Estimate"].apply(
    lambda x: 1 if 'employer provided' in x.lower() else 0)

df = df[df["Salary Estimate"] != '-1']
salary = df["Salary Estimate"].apply(lambda x: x.split('(')[0])
minus_kdollar = salary.apply(lambda x: x.replace('K', '').replace('$', ''))
min_hr = minus_kdollar.apply(lambda x: x.lower().replace(
    'per hour', '').replace('employer provided', ''))

df["min_salary"] = min_hr.apply(lambda x: x.split("-")[0])
df["max_salary"] = min_hr.apply(lambda x: x.split("-")[1])

# Company text cleaning
df["Company Text"] = df.apply(lambda x: x["Company Name"] if float(
    x["Rating"]) < 0 else x["Company Name"][:-3], axis=1)

# State Cleaning
df["Job State"] = df["Location"].apply(lambda x: x[-2:])
df["Job State"].value_counts()
# If head office and location are same then 1 else 0
df["Same state"] = df.apply(
    lambda x: 1 if x.Location == x.Headquarters else 0, axis=1)

# Age of the Company
df["age"] = df.Founded.apply(lambda x: x if x < 1 else datetime.datetime.now().year - x)

# Job Description
#python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df.python_yn.value_counts()

# R studio
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df.R_yn.value_counts()

# Spark
df['spark_yn'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark_yn.value_counts()

# AWS
df['aws_yn'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws_yn.value_counts()

# excel
df['excel_yn'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.excel_yn.value_counts()

# df.columns
df_out  = df.drop(["Unnamed: 0"], axis=1)
df_out.to_csv('salary_cleaned_data.csv', index=False)
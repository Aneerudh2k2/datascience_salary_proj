# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 12:23:17 2023

@author: Admin
"""

import pandas as pd
import numpy as np

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
df["Company Text"] = df.apply(lambda x: x["Company Name"] if float(x["Rating"]) < 0 else x["Company Name"][:-3], axis=1)



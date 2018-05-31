# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np 

#data = pd.read_csv('Position_Salaries.csv)
#data1 =data.groupby(['Level','Position']).sum()
#data2= data.swaplevel('Level','Position')
#print(data1)

Dataset = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data')

print(Dataset.head())

Dataset.columns=["age","workclass","fnlwgt","education","education_num","marital_status","occupation","relationship","race","sex","capital_gain","capital_loss","hours_per_week","native_country","Salary-Slab"]


print(Dataset.head())
print('='*34)
print('Sql Connection and creating DB')
import sqlalchemy
import sqlite3

from sqlalchemy import create_engine

engine = create_engine('sqlite:///sqladb', echo=False)

Dataset.to_sql('sqladb', engine, if_exists='replace')
connection = sqlite3.connect("sqladb")
cmd = connection.cursor()
print('1. Select 10 records from the adult sqladb')
print(pd.read_sql_query('SELECT * FROM sqladb limit 10', connection))

print('2. Show me the average hours per week of all men who are working in private sector')
print(pd.read_sql_query("SELECT Avg(hours_per_week) as [Average for men in private Sector] FROM sqladb where sex=' Male' and workclass=' Private' ", connection).head())

#print('3.Show me the frequency table for education, occupation and relationship, separately')

print('3.Show me the frequency table for education, occupation and relationship, separately')

print('\n##','For education','##\n')
print(pd.read_sql_query("SELECT education ,count(*) as frequency FROM sqladb group by education", connection))

print('\n##','For occupation','##\n')
print(pd.read_sql_query("SELECT occupation ,count(*) as frequency FROM sqladb group by occupation", connection))

print('\n##','For relationship','##\n')
print(pd.read_sql_query("SELECT relationship ,count(*) as frequency FROM sqladb group by relationship", connection))
#4. Are there any people who are married, working in private sector and having a masters
#degree
print('\n4.people who are married, working in private sector and having a masters degree')
print(pd.read_sql_query("select count(*)  from sqladb where workclass=' Private' and marital_status=' Married-civ-spouse' and education=' Masters' ",connection).head())

print('\n5. What is the average, minimum and maximum age group for people working in different sectors')
print(pd.read_sql_query("SELECT occupation,avg(age) AS [Average Age],"+ 
               " max(age) AS [Maximum Age],"+ 
               " min(age) AS [Minimum Age] "+ 
               " FROM sqladb "+
               " GROUP BY occupation",connection))

#6. Calculate age distribution by country
print('\n6. Calculate age distribution by country')
print(pd.read_sql_query("SELECT native_country,avg(age) AS [Average Age],"+ 
               " max(age) AS [Maximum Age],"+ 
               " min(age) AS [Minimum Age] "+ 
               " FROM sqladb "+
               " GROUP BY native_country",connection))

print('\nAdditional 6. Calculate age distribution by country(India)')
print(pd.read_sql_query("SELECT native_country,age ,"+ 
               " count(*) AS [Count of Age]"+ 
               " FROM sqladb where native_country=' India' "+
               " GROUP BY native_country,age",connection))

print('\n7. Compute a new column as "Net-Capital-Gain" from the two columns "capital-gain" and '+
'"capital-loss"')
cmd.execute('Alter table sqladb'+
            '  Add net_capital_gain int')

cmd.execute('UPDATE sqladb SET net_capital_gain=capital_gain-capital_loss')
print(pd.read_sql_query('SELECT * FROM sqladb limit 10', connection))

import pandas as pd

#Loading data or importing data
dataset = pd.read_csv('ml.csv')

#Describing data frame
print(dataset.head())
print(dataset.tail())
print(dataset.info())
print(dataset.describe())

#printing 
print(dataset.isnull().sum())

#Data preprocessing


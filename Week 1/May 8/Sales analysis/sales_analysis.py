import pandas as pd

df = pd.read_csv('retail_sales_dataset.csv')   #dataset downloaded from kaggle
print("\nFirst few rows of dataset are : \n",df.head())
print("\nLast few rows of dataset are : \n",df.tail())

print("\n\nThe columns of dataset are : \n",df.columns)

print("\n\nThe shape of dataset are : \n",df.shape)

print("\n\nThe statistics of dataset are : \n",df.describe())

print("\nDataset Info:")
print(df.info())

print("\n\nThe data types are : \n",df.dtypes)

print("\n\nThe missing values of each rows are : \n",df.isnull().sum()) 

print("\nTotal missing values : ",df.isnull().sum().sum())
print("\n\n") 



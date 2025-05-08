import pandas as pd
import numpy as np

df = pd.read_csv("retail_sales_dataset.csv") 
df = df.dropna()

avg_sales = df.groupby('Product Category')['Total Amount'].mean().sort_values()
print("\nAverage Sales by Product Category : \n",avg_sales)

print(f"Mean: {np.mean(df['Total Amount'])}")
print(f"Median: {np.median(df['Total Amount'])}")
print(f"Standard Deviation: {np.std(df['Total Amount'])}")
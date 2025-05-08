import pandas as pd

import matplotlib.pyplot as plt

df = pd.read_csv("retail_sales_dataset.csv") 
df = df.dropna()

avg_sales = df.groupby('Product Category')['Total Amount'].mean().sort_values()

plt.figure(figsize=(10, 6))
bars = plt.bar(avg_sales.index, avg_sales.values, color='skyblue')
plt.title('Average Sales Amount by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Average Total Amount')
plt.grid(axis='y', linestyle='--',alpha=0.3)

for bar in bars:
    y_value = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, y_value, f'{y_value:.2f}', va='bottom', ha='center')

plt.show()

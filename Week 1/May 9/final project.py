import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class RetailSalesAnalysis:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.file_path)
        print("\nFirst few rows of dataset:\n", self.df.head())
        print("\nLast few rows of dataset:\n", self.df.tail())
        print("\nColumns in dataset:\n", self.df.columns)
        print("\nShape of dataset:\n", self.df.shape)
        print("\nDescriptive statistics:\n", self.df.describe())
        print("\nDataset Info:")
        print(self.df.info())
        print("\nData types:\n", self.df.dtypes)
        print("\nMissing values per column:\n", self.df.isnull().sum())
        print("\nTotal missing values in dataset:", self.df.isnull().sum().sum())

    def clean_data(self):
        print("\nCleaning data by dropping rows with missing values\n")
        self.df.dropna(inplace=True)

    def analyze_sales(self):
        print("\nSales analysis\n")
        avg_sales = self.df.groupby('Product Category')['Total Amount'].mean().sort_values()
        print("\nAverage Sales by Product Category:\n", avg_sales)
        print(f"\nMean of Total Amount: {np.mean(self.df['Total Amount'])}")
        print(f"Median of Total Amount: {np.median(self.df['Total Amount'])}")
        print(f"Standard Deviation of Total Amount: {np.std(self.df['Total Amount'])}")
        return avg_sales

    def plot_sales(self, avg_sales):
        print("\nPlotting average sales\n")
        plt.figure(figsize=(10, 6))
        bars = plt.bar(avg_sales.index, avg_sales.values, color='skyblue')
        plt.title('Average Sales Amount by Product Category')
        plt.xlabel('Product Category')
        plt.ylabel('Average Total Amount')
        plt.grid(axis='y', linestyle='--', alpha=0.3)

        for bar in bars:
            y_value = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, y_value, f'{y_value:.2f}',
                     va='bottom', ha='center')

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    analyzer = RetailSalesAnalysis("C:/Users/gadha/OneDrive/Desktop/KLAW-APP-Internship/Week 1/May 9/retail_sales_dataset.csv")

    analyzer.load_data()
    analyzer.clean_data()
    avg_sales = analyzer.analyze_sales()
    analyzer.plot_sales(avg_sales)

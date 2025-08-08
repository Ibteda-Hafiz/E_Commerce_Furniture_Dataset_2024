# E-Commerce Furniture Dataset 2024
This project focuses on analyzing an e-commerce furniture dataset through exploratory data analysis (EDA) and predictive modeling. The initial phase involved data cleaning, which included loading the dataset, addressing missing values in the tagText column by imputing with the most frequent value, and standardizing the price and sold columns by converting them to numerical types and removing irrelevant characters like '$' and ','. After cleaning, the dataset's integrity was confirmed by checking for remaining missing values and reviewing data types.
# Dataset Description
This dataset, ecommerce_furniture_dataset_2024.csv, contains information about e-commerce furniture products. It includes the following columns:
1)productTitle: The title of the furniture product.
2)originalPrice: The original price of the product (contains missing values).
3)price: The current price of the product.
4)sold: The number of units of the product sold.
5)tagText: Text tags associated with the product, potentially indicating promotions or features.
# Analysis Objectives
Here are the objectives performed in this project:
1)Cleaned the dataset by handling missing values and converting data types.
2)Explored the relationship between product price and the number of items sold.
3)Analyzed the average items sold based on product tags.
4)Examined the distribution of product prices.
5)Generated summary statistics for numerical columns.
6)Built a Linear Regression model to predict the number of items sold.
7)Evaluated the performance of the predictive model.
# Technologies Used
1)Python: The primary programming language used for the analysis.
2)pandas: Used for data loading, cleaning, and manipulation.
3)matplotlib: Used for creating static, interactive, and animated visualizations.
4)seaborn: Used for creating statistical graphics.
5)scikit-learn: Used for building and evaluating the predictive model (Linear Regression).
6)Google Colab: The environment where the notebook was executed.

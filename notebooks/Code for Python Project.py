# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 04:22:08 2024

@author: Willi
"""

#Load the dataset and import as dataframe
#I would store my dataframe as df_Superstore
import pandas as pd
df_Superstore = pd.read_csv('C:/Users/Willi/OneDrive/Documents/business analytics/Project/Superstore - Sales Original.csv')

#Checking the data information
df_Superstore.info() 

# Checking for missing values
Missingvalues = df_Superstore.isnull().sum()
print(Missingvalues) #Display total Missing values

#Check for duplicated values
Duplicatedvalues = df_Superstore.duplicated().sum()
print(Duplicatedvalues) #Display Total Duplicated Values

# Create a new DataFrame with only the selected columns 
#df_store = df_Superstore[columns_to_keep] 

df_Superstore['Order Date'] = pd.to_datetime(df_Superstore['Order Date'], errors='coerce')
# Add a new column, quarter, based on the time column, in order to look at our sales on a quarterly basis.
df_Superstore['Quarter'] = df_Superstore['Order Date'].dt.to_period('Q') 
# Calculate the accurate quarter based on the 'date' column 
#addd new column called year
df_Superstore['Year'] = df_Superstore['Order Date'].dt.to_period('Y')

df_Superstore['Discount'] = df_Superstore['Discount'].str.replace('%', '').astype(float) / 100

Total_Sales= df_Superstore[['Sales']].sum() #Calculating for total sales
#Store and use selected numerical columns by not using the ones mentioned.
N=df_Superstore.drop(columns=['Quarter','Year','Row ID','State','Category', 'Quarter','Order ID', 'Order Date', 'Ship Date', 'Sub-Category', 'Product ID', 'Product Name','Customer ID','Postal Code','Region', 'Country','City', 'Ship Mode'])


# Create a summary matrix
Summary_Stat = pd.DataFrame({
    'mean': N.mean(),
    'median': N.median(),
    'std': N.std(),
    'max': N.max(),
    'min': N.min(),
    '25% (Q1)': N.quantile(0.25),
    '75% (Q3)': N.quantile(0.75)
})

print(Summary_Stat) #Display results


### calculating the 25% quantile and 75% quantile 

Q1 = df_Superstore[['Profit','Sales','Quantity','Discount','CoGS']].quantile(0.25)
Q3 = df_Superstore[['Profit','Sales','Quantity','Discount','CoGS']].quantile(0.75)
#### To get the outlier i calculated the interquantile range
IQR = Q3 - Q1

# to identify the lower and upper bound to which the each variable should not exceed
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR


## to show the relationship between the numerical data we use the correlation matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Calculate correlation matrix
correlation_matrix = N.corr()

####### We create a categorical-categorical relationship
###### Show the relationship between the Category and the region
Category = ['Office Supplies', 'Furniture', 'Technology']
Region = df_Superstore.pivot_table(values='Quarter', index='Category', 
                                  columns='Region', aggfunc='count')
Region.plot(kind='bar', figsize=(8, 5)) 
plt.ylabel("Count") 
plt.show()


###Sub v Region
Region = ['Central', 'East', 'West', 'South']
Sub_Category = df_Superstore.pivot_table(index ='Sub-Category',
                                  values='Category', columns ='Region',aggfunc='count')
Sub_Category.plot(kind='bar', figsize=(8, 5))
plt.legend(loc='upper left', fontsize='x-small')
plt.ylabel("Count") #Naming the y axis
plt.xlabel("Subategory")#naming the x axis
plt.show() #Display the graph

## Numeric on Numeric
# Scatter plot for Sales vs. Profit 
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df_Superstore.Sales, y=df_Superstore.Profit, color='teal')
plt.title('Sales vs. Profit', fontsize=14)
plt.xlabel('Sales')
plt.ylabel('Profit')
plt.grid(True)

## Scatter plot for Quantity vs. Profit
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df_Superstore.Quantity, y=df_Superstore.Sales, color='teal')
plt.title('Quantity vs. Profit', fontsize=14)
plt.xlabel('Quantity')
plt.ylabel('Profit')
plt.grid(True)

# Scatter plot for Quantity vs. Sales
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df_Superstore.Quantity, y=df_Superstore.Sales, color='teal')
plt.title('Quantity vs. Sales', fontsize=14)
plt.xlabel('Quantity')
plt.ylabel('Sales')
plt.grid(True)


#Time series sales v year
Year = df_Superstore.pivot_table(values=['Sales','Profit', 'Quantity','CoGS'], index='Year', 
                                  aggfunc='sum')
Year.plot()

#### We start with the categorical vrs numerical relationship
#### 1 Relationship between state and the sales 
#Best Performing state interms of Sales v Worse
SS = df_Superstore.pivot_table(values='Sales',  index='State',aggfunc = 'sum')
AS = SS.sort_values(by='Sales', ascending=False)
# Creating a horizontal bar plot
plt.figure(figsize=(10, 8))  # Adjust figure size
AS.plot(kind='bar', legend=True, color='yellow', alpha=0.8)

# Summing sales by state V PROFIT. The best Performing state V worst
CP = df_Superstore.pivot_table(values='Profit', index='State', aggfunc='sum')# 
AP = CP.sort_values(by='Profit', ascending=False) #Arrnaging the graph from the largest to lowest
#CP.plot(kind='bar')
# Creating a horizontal bar plot
plt.figure(figsize=(20, 15))  # Increase width and height
AP.plot(kind='bar', legend=True, color='red', alpha=0.8) #Selecting and displaying the particular type of visuals I want, i.e bar chart

##### showing the relationship of which category has the highest Sales and Profit
B = df_Superstore.pivot_table(values=['Sales', 'Profit','Quantity'], index='Category', aggfunc='sum')
B.plot(kind='bar')#Selecting and displaying the particular type of visuals I want, i.e bar chart

#showing the relationship of which Region has the highest Sales and Profit and Quantity demand
W = df_Superstore.pivot_table(values=['Sales', 'Profit','Quantity'], index='Region', aggfunc='sum')
W.plot(kind='bar')#Selecting and displaying the particular type of visuals I want, i.e bar chart

# Sales and Profit based on Subcategory
C = df_Superstore.pivot_table(values=['Sales', 'Profit'], index='Sub-Category', aggfunc='sum')
C = C.sort_values(by=['Sales','Profit'], ascending=False)
C.plot(kind='bar') #Selecting and displaying the particular type of visuals I want, i.e bar chart












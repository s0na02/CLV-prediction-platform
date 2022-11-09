# CLV-prediction-platform

## Why CLV?

CLV prediction is part of Customer Relationship Management system which is an information management and analysis tool that can help businesses and other organizations manage their interactions with customers.
Customer data is collected in a CRM database, which allows for advanced analysis such as CLV for customer segmentation.
Businesses can manage marketing decisions based on CLV predictions.
They can also manage risks related to customers.

## Dataset

### Dataset Information

Dataset is taken from UCI (https://archive.ics.uci.edu/ml/datasets/online+retail#). 
This international dataset includes every transaction made by a UK-based internet retailer between December 1, 2010, and December 9, 2011. The company primarily offers unique gifts for every occasion. The company has a large number of wholesalers as clients.

### Data Description

Dataset contains 8 attributes. You can find description of each down below:

**InvoiceNo** - _6-digit unique number assigned to each transaction. If code starts with 'c', it indicates a cancellation._

**StockCode** - _Product code is a 5-digit unique number assigned to each product._                                                    

**Description** - _Product name_                                                                                                                

**Quantity** - _The quantities of each product per transaction. _                                                                             

**InvoiceDate** - _The date and time when each transaction was generated._                                                                       

**UnitPrice** - _Product price per unit._

**CustomerID** - _Customer number is a 5-digit unique number assigned to each customer._

**Country** - _Customer's residence country._

### Data Preperation

For data preperation stage our group cleaned the data and also created new features that will be needed in later stages for calculating the CLV.

For cleaning the data, we removed all the duplicates.

For **Quantity**, we will consider only positive quantities, as negative values indicate that the product was returned for some reason.

**Total Purchase** = **UnitPrice** x **Quantity**

**Avg order value** =  money spent / number of transactions

**Purchase Frequency** = average number of orders from each customer

**Churn Rate** = the percentage of customers who have not ordered again

**CLTV** = (Average Order Value x Purchase Frequency) / Churn Rate



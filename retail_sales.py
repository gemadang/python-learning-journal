'''
Imagine you work for a retail company that needs to process sales records. Each record contains:

A unique sale ID.
A sale date.
The amount of the sale.
The product name sold.
Your program will offer the options to:

Load in sales data (reading from a CSV or database).
Retrieve the latest sale
Compute the total revenue
Check for duplicate sale IDs 
Search for a sale by its ID
You will measure the performance of these operations and compare them against their theoretical Big O time complexity. 
'''

import csv
from datetime import datetime, date

class RetailCompany:
    def __init__(self, sales_data):

        self.sales_data = sales_data
        #process sales data and make map
        self.sales_map = {}
        self.duplicates = {}

        with open("./" + sales_data, 'r') as file:
            csvreader = csv.reader(file)

            skip_first_row = False
            headers = []
            for row in csvreader:
                if not skip_first_row:
                    # first row is the column headers so we can skip that
                    skip_first_row = True
                    # sale_id,sale_date,amount,product
                    headers = row
                else:
                    sale_id = int(row[0])

                    row_map = {}
                    for i, header in enumerate(headers):
                        row_i = row[i]                        
                        row_map[header] = row_i

                    if sale_id in self.sales_map: #means there is a duplicate
                        if sale_id in self.duplicates: #there was already a duplicate
                            self.duplicates[sale_id].append(row_map)
                        else: #first duplicate found, doucument both duplicates
                            self.duplicates[sale_id] = [self.sales_map[sale_id], row_map]
            
                    # will store latest sale_id in map
                    self.sales_map[sale_id] = row_map

    def convert_date_string(self, date_string):
        row_date_strip = date_string.split('-')
        year = int(row_date_strip[0])
        month = int(row_date_strip[1])
        day = int(row_date_strip[2])
        return datetime(year, month, day)

    def latest_sale(self,include_duplicates=False):
        max_date = datetime(1,1,1)
        latest_sale = None
        for sale in self.sales_map:
            new_date = self.convert_date_string(self.sales_map[sale]['sale_date'])

            if include_duplicates and sale in self.duplicates:
                for sale_row in self.duplicates[sale]:
                    new_date = self.convert_date_string(sale_row['sale_date'])
                    if new_date > max_date:
                        max_date = new_date
                        latest_sale = [sale_row]
                    elif new_date is max_date: 
                        latest_sale.append(sale_row)
            else:
                if new_date > max_date:
                    max_date = new_date
                    latest_sale = [self.sales_map[sale]]
                elif new_date is max_date: 
                    latest_sale.append(self.sales_map[sale])

        return latest_sale

    def total_revenue(self, include_duplicates=False):
        total_revenue = 0
        for sale in self.sales_map:
            amount = float(self.sales_map[sale]['amount'])

            if include_duplicates and sale in self.duplicates:
                for sale_row in self.duplicates[sale]:
                    amount = float(sale_row['amount'])
                    total_revenue += amount
            else:
                total_revenue += amount

        return total_revenue

    def get_duplicate(self, sale_id):
        if sale_id not in self.duplicates:
            print('no duplicate found')
        else:
            print('found duplicate sales')
            return self.duplicates[sale_id]

    def check_duplicates(self):
        if not self.duplicates: #duplicates list is empty
            print('no duplicates')
            return False
        else:
            for sale_id in self.duplicates:
                print(self.get_duplicate(sale_id))
            return True

    def find_sale(self, sale_id):
        sale_id = int(sale_id)
        if sale_id in self.duplicates:
            return self.get_duplicate(sale_id)
        if sale_id not in self.sales_map:
            return False
        return self.sales_map[sale_id]

my_retail_company = RetailCompany('./sales_data.csv')
sale = my_retail_company.find_sale(9)
is_there_duplicates = my_retail_company.check_duplicates()
revenue = my_retail_company.total_revenue()
revenue_dup = my_retail_company.total_revenue(True)
latest = my_retail_company.latest_sale()

# print(my_retail_company.sales_map)
print(latest)

'''
Reflection
After running your pipeline with different input sizes, consider the following:

Performance Trends:

How does each operation's execution time change as the dataset grows?
All are O(n) except finding the sale

Do the results align with the theoretical Big O expectations?
yes
Real-World Implications:

Which steps might become bottlenecks in a production system processing millions of records?
the duplication steps i made 

How would you optimize or replace the inefficient (quadratic) approach?
for the duplicates if you compare each sale with one anohter for not jsut the sasle id but other data variables you might have to create different maps

Practical Adjustments:

How might you put together a testing plan for this project?
using unittest i can create tests that run through all functionaities with different data set examples

What additional error handling or data validation would be necessary?
checking if the file exists or if data isnt in the expected format
'''
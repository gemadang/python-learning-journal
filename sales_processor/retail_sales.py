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

'''
    You will need to generate python code to randomly generate n number of data to store in a CSV 
    for testing purposes. 
    You will measure the time each operation takes at dataset sizes of 100, 1.000, 10.000, and 100.000 
    (if possible) and graph your results.
'''

import csv
import random
from datetime import datetime, date
import unittest


'''
    Sales Data Manager class

    Generate sales data csv
'''
class SalesDataManager:
    def __init__(self, n=100):

        self.headers = ['sale_id', 'sale_date', 'amount', 'product']
        self.folder = './sales_data/'
        self.created_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        self.sale_id_map = {}

        self.max_date = datetime(1,1,1)
        self.latest_sales = []
        self.duplicates = []
    
        if type(n) is int:
            self.synthesize_data(n)
        elif type(n) is str:
            # deconstruct full path
            full_path = self.deconstruct_full_path(n)
            try:
                #load csv file
                with open(full_path, 'r', newline='') as file:
                    csv_file = csv.DictReader(file)
                    for lines in csv_file:
                        self.add_sale_to_map(lines)                    
            except csv.Error:
                print('CSV file not found')
        
        #get biggest id number 
        max_id = max(list(self.sale_id_map))
        #add duplicates with new ids
        for i, dupe in enumerate(self.duplicates):
            dupe['sale_id'] = str(max_id+i+1)
            self.add_sale_to_map(dupe)

    def convert_date_string_to_date_time(self, date_string):
        row_date_strip = date_string.split('-')
        year = int(row_date_strip[0])
        month = int(row_date_strip[1])
        day = int(row_date_strip[2])
        return datetime(year, month, day)

    def add_sale_to_map(self,row):
        sale_id = int(row['sale_id'])
        sale_date = self.convert_date_string_to_date_time(row['sale_date'])

        #everytime a sale is added to a map check if its the latest sale
        if sale_date > self.max_date:
            self.max_date = sale_date
            self.latest_sales = [row]
        elif sale_date is self.max_date: 
            self.latest_sales.append(row)

        # everytime data is loaded in, check for duplicates 
        # duplicate will be included at the as new ids 
        if sale_id in self.sale_id_map: # means there is a duplicate
            self.duplicates.append(row)

        #add sale data to map
        self.sale_id_map[sale_id] = row


    def get_sale(self, sale_id):
        sale_id = int(sale_id)
        return self.sale_id_map[sale_id]

    def get_latest_sale(self):
        return self.latest_sales
    
    def sum_amounts(self):
        total_amount = 0
        for sale in self.sale_id_map:
            amount = float(self.sale_id_map[sale]['amount'])
            total_amount += amount
        return "{:.2f}".format(round(total_amount,2))

    def deconstruct_full_path(self, full_path):
        #file name (# of items)_sales_data_(datetime created)
        self.full_path = full_path
        self.file_name = full_path.replace(self.folder, '')
        return self.full_path
    
    def construct_full_path(self, n, date):
        #file name (# of items)_sales_data_(datetime created)
        
        self.file_name = str(n)+'_sales_data_'+ date.replace(' ','-')+'.csv'
        self.full_path = self.folder + self.file_name
        return self.full_path

    def synthesize_data(self, n):
        # create csv

        file_path = self.construct_full_path(n, self.created_date)

        with open(file_path, 'w', newline='') as file:
            # write to csv
            file_write = csv.writer(file)

            # insert headers
            file_write.writerow(self.headers)
            
            # generate data
            for i in range(n):
                sale_id = i
                sale_date = self.generate_date()
                amount = self.generate_amount()
                product = self.generate_product()

                #map to access sale_id
                sale_data_row = {
                    'sale_id': sale_id,
                    'sale_date': sale_date,
                    'amount': amount,
                    'product': product
                    }
                self.add_sale_to_map(sale_data_row)

                row = [sale_id,sale_date,amount,product]
                row_joined= ','.join(str(x) for x in row)
            
                file_write.writerow(row)

    def generate_date(self):
        start_date = datetime(1996, 5, 4)
        end_date = datetime.now()
        random_date = start_date + (end_date - start_date) * random.random()
        return random_date.strftime('%Y-%m-%d')

    def generate_amount(self):
        return "{:.2f}".format(round(random.random()*300 + 50, 2))

    def generate_product(self):
        return random.choice(['Widget', 'Gadget', 'Thingamajig', 'Doohickey', 'Kazoobob'])


'''
    Retail Company class 

    latest_sale
    total_revenue
    find_sale
'''
class RetailCompany:
    def __init__(self, sales_data_manager):
        self.sales_data_manager = sales_data_manager
        self.sales_data = sales_data_manager.sale_id_map
        self.sales_data_path = sales_data_manager.full_path

    def latest_sale(self):
        return self.sales_data_manager.get_latest_sale()

    def total_revenue(self):
        return float(self.sales_data_manager.sum_amounts())

    def find_sale(self, sale_id):
        return self.sales_data_manager.get_sale(sale_id)

class TestRetailCompany(unittest.TestCase):
    def setUp(self):
        self.small_sales_data_manager = SalesDataManager(100)
        self.small_retail_company = RetailCompany(self.small_sales_data_manager)

        self.medium_sales_data_manager = SalesDataManager(1000)
        self.medium_retail_company = RetailCompany(self.medium_sales_data_manager)

        self.large_sales_data_manager = SalesDataManager(10000)
        self.large_retail_company = RetailCompany(self.large_sales_data_manager)

        self.xlarge_sales_data_manager = SalesDataManager(10000)
        self.xlarge_retail_company = RetailCompany(self.xlarge_sales_data_manager)

    def test_find_sale(self):
        self.assertIsNotNone(self.small_retail_company.find_sale(99))
        self.assertIsNotNone(self.medium_retail_company.find_sale(999))
        self.assertIsNotNone(self.large_retail_company.find_sale(9999))
        self.assertIsNotNone(self.xlarge_retail_company.find_sale(9999))
    
    def test_total_revenue(self):
        self.assertGreaterEqual(self.small_retail_company.total_revenue(), 0)
        self.assertGreaterEqual(self.medium_retail_company.total_revenue(), 0)
        self.assertGreaterEqual(self.large_retail_company.total_revenue(), 0)
        self.assertGreaterEqual(self.xlarge_retail_company.total_revenue(), 0)
    
    def test_latest_sale(self):
        self.assertIsNotNone(self.small_retail_company.latest_sale())
        self.assertIsNotNone(self.medium_retail_company.latest_sale())
        self.assertIsNotNone(self.large_retail_company.latest_sale())
        self.assertIsNotNone(self.xlarge_retail_company.latest_sale())

if __name__ == "__main__":
    unittest.main()

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
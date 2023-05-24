import ast
import math
import random
import time
from datetime import datetime
import matplotlib.pyplot as plt
from model_order import Order
from model_product import Product
from opreation_product import ProductOperation


class OrderOperation(ProductOperation):
    order_list =[]
    customer_list =[]
    def generate_unique_order_id(self):
        # Read the existing orders from the file
        with open('data/orders.txt', 'r') as file:
            orders = file.readlines()

        # Generate a new order ID
        order_id = len(orders) + 1
        order_id_str = f"o_{order_id:05}"

        return order_id_str

    def create_an_order(self, customer_id, product_id, create_time=None,price=0):
        # Generate a unique order ID
        order_id = self.generate_unique_order_id()

        # Get the current time if create_time is not provided
        if create_time is None:
            create_time = time.strftime("%d-%m-%Y_%H:%M:%S")

        # Create the order data
        order_data = f"{{'order_id':'{order_id}', 'customer_id':'{customer_id}', 'product_id':'{product_id}', 'create_time':'{create_time}'}}\n"
        order =Order(order_id,customer_id,product_id,create_time,price)

        try:
            # Append the order data to the file
            with open('data/orders.txt', 'a') as file:
                file.write(order_data)

            return True
        except Exception as e:
            print(f"Failed to create order: {e}")
            return False

    def delete_order(self, order_id):
        # Read the existing orders from the file
        orders = self.read_orders_from_file()

        # Find the order with the provided order_id
        for order in orders:
            if order['order_id'] == order_id:
                # Remove the order from the list
                orders.remove(order)

                # Write the updated list of orders back to the file
                self.write_orders_to_file(orders)

                return True

        return False


    def write_orders_to_file(self, orders):
        with open('data/orders.txt', 'w') as file:
            for order in orders:
                file.write(str(order) + "\n")

    def get_order_list(self, customer_id, page_number):
        # Read the existing orders from the file
        orders = self.read_orders_from_file()

        if customer_id ==0:
            customer_orders = [order for order in orders]
        else:
            # Filter orders for the given customer_id
            customer_orders = [order for order in orders if order['customer_id'] == customer_id]

        # Calculate the total number of pages
        total_pages = math.ceil(len(customer_orders) / 10)

        # Calculate the start and end indices for the current page
        start_index = (page_number - 1) * 10
        end_index = start_index + 10

        # Retrieve orders for the current page
        page_orders = customer_orders[start_index:end_index]

        return page_orders, page_number, total_pages

    def read_orders_from_file(self):
        try:
            with open('data/orders.txt', 'r') as file:
                orders = [eval(line) for line in file]
            return orders
        except FileNotFoundError:
            return []

    def generate_test_order_data(self):
        customers = self.customer_list
        products = self.product_data

        # Generate orders for each customer
        for customer in customers:
            num_orders = random.randint(50, 200)

            for _ in range(num_orders):
                # Generate random order details
                order_id = self.generate_unique_order_id()
                product = random.choice(products)
                create_time = self.generate_random_order_time()

                # Create the order
                self.create_an_order(customer.user_id, product.pro_id, create_time,product.pro_raw_price)

    # def generate_unique_order_id(self):
    #     # Implement this method to generate a unique order id
    #     # You can use any logic to generate a unique order id
    #     return "o_" + str(random.randint(10000, 99999))

    def generate_random_order_time(self):
        # Generate a random order time scattered into different months of the year
        year = datetime.now().year
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        order_time = datetime(year, month, day, hour, minute, second)
        return order_time

    # def read_orders_from_file_s(self):
    #     # Read the orders from the file and return a list of order objects
    #
    #     with open('data/orders.txt', 'r') as file:
    #         for line in file:
    #             order_data = line.strip().split(',')
    #             # Create an Order object based on the order_data and add it to the list
    #             order = Order(order_data[0], order_data[1], order_data[2], order_data[3])
    #             self.order_list.append(order)
    #     return self.order_list

    def read_orders_from_file_s(self):
        # Read the orders from the file and return a list of order objects
        self.order_list = []  # Clear the order list before reading new orders

        with open('data/orders.txt', 'r') as file:
            for line in file:
                order_data = ast.literal_eval(line.strip())
                # Create an Order object based on the order_data and add it to the list
                order = Order(order_data['order_id'], order_data['customer_id'], order_data['product_id'],
                              order_data['create_time'])
                order.price=self.get_product_by_id(order_data['product_id']).pro_raw_price
                self.order_list.append(order)

        return self.order_list

    def write_orders_to_file_s(self, orders):
        # Write the list of orders to the file
        with open('data/orders.txt', 'w') as file:
            for order in orders:
                # Write the order details to the file in the desired format
                file.write(f"{order.order_id},{order.customer_id},{order.product_id},{order.create_time}\n")

    def generate_single_customer_consumption_figure(self, customer_id):
        # Read all orders from the file
        orders = self. read_orders_from_file_s()

        # Filter orders for the given customer_id
        customer_orders = [order for order in orders if order.user_id == customer_id]

        # Calculate the monthly consumption
        monthly_consumption = {}
        for order in customer_orders:
            order_time = datetime.strptime(order.order_time, "%Y-%m-%d %H:%M:%S")
            month = order_time.month
            if month in monthly_consumption:
                monthly_consumption[month] += order.price
            else:
                monthly_consumption[month] = order.price

            # Sort the monthly consumption by month
        sorted_monthly_consumption = sorted(monthly_consumption.items())

        # Extract the months and consumption values
        months = [month for month, _ in sorted_monthly_consumption]
        consumption = [consumption for _, consumption in sorted_monthly_consumption]

        # Create a line chart to visualize the monthly consumption for all customers
        plt.plot(months, consumption, marker='o')
        plt.xlabel('Month')
        plt.ylabel('Consumption')
        plt.title('Monthly Consumption for All Customers')
        plt.show()

    from datetime import datetime

    def generate_all_customers_consumption_figure(self):
        # Read all orders from the file
        orders = self.order_list.copy()

        # Calculate the monthly consumption for all customers
        monthly_consumption = {}
        for order in orders:
            order_time = datetime.strptime(order.order_time, "%Y-%m-%d %H:%M:%S")
            month = order_time.month
            if month in monthly_consumption:
                monthly_consumption[month] += order.price
            else:
                monthly_consumption[month] = order.price

        # Sort the monthly consumption by month
        sorted_monthly_consumption = sorted(monthly_consumption.items())


        # Extract the months and consumption values
        months = [month for month, _ in sorted_monthly_consumption]
        consumption = [consumption for _, consumption in sorted_monthly_consumption]

        # Create a line chart to visualize the monthly consumption for all customers
        plt.plot(months, consumption, marker='o')
        plt.xlabel('Month')
        plt.ylabel('Consumption')
        plt.title('Monthly Consumption for All Customers')
        plt.show()

    def generate_all_top_10_best_sellers_figure(self):
        # Read all products from the file
        products = self.read_products_from_file()

        # Sort the products by their sales count in descending order
        sorted_products = sorted(products, key=lambda product: product.sales_count, reverse=True)

        # Get the top 10 best-selling products
        top_10_best_sellers = sorted_products[:10]

        # Extract the product names and their sales count
        product_names = [product.pro_name for product in top_10_best_sellers]
        sales_count = [product.pro_likes_count for product in top_10_best_sellers]

        # Create a bar chart to visualize the top 10 best-selling products
        plt.bar(product_names, sales_count)
        plt.xlabel('Product')
        plt.ylabel('Sales Count')
        plt.title('Top 10 Best-Selling Products')
        plt.xticks(rotation=90)
        plt.show()

    def read_products_from_file(self):
        # Read the products from the file and return a list of product objects
        products = []
        with open('data/products.txt', 'r') as file:
            for line in file:
                product_data = line.strip().split(',')
                # Create a Product object based on the product_data and add it to the list
                product = Product(product_data[0], product_data[1], product_data[2], ...)
                products.append(product)
        return products

    def delete_all_orders(self):
        # Open the orders file in write mode to clear its content
        with open('data/orders.txt', 'w') as file:
            file.truncate()

import glob
import csv
import matplotlib.pyplot as plt
from model_product import Product
import os

product_data = []


class ProductOperation:
    def extract_products_from_files(self):
        global product_data

        # Extract product information from csv files
        file_paths = glob.glob("data/product/*.csv")

        for file_path in file_paths:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    p = Product(row['id'], row['model'], row['category'], row['name'], row['current_price'],
                                row['raw_price'], row['discount'], row['likes_count'])

                    product_data.append(p)

        # Write the extracted product information to the file
        with open('data/products.txt', 'w') as file:
            for product_info in product_data:
                file.write(str(product_info) + "\n")

        print("Product information extracted and saved successfully.")

    def get_product_list(self, page_number):
        global product_data

        products_per_page = 10
        total_products = len(product_data)
        total_pages = (total_products + products_per_page - 1) // products_per_page

        if page_number < 1 or page_number > total_pages:
            return [], 0, 0

        start_index = (page_number - 1) * products_per_page
        end_index = start_index + products_per_page

        products = product_data[start_index:end_index]

        return products, page_number, total_pages

    def delete_product(self, product_id):
        global product_data

        # Find the product with the provided product_id
        for product in product_data:
            if product.pro_id == product_id:
                # Remove the product from the list
                product_data.remove(product)

                # Write the updated list of products back to the file
                with open('data/products.txt', 'w') as file:
                    for product in product_data:
                        file.write(str(product) + "\n")

                return True

        return False

    def get_product_list_by_keyword(self, keyword):
        global product_data

        # Filter the products based on the keyword
        matching_products = [product for product in product_data if keyword.lower() in product.pro_name.lower()]

        return matching_products

    def get_product_by_id(self, product_id):
        global product_data

        # Search for the product with the given product_id
        for product in product_data:
            if product.pro_id == product_id:
                return product

        return None

    class ProductOperation:
        def generate_category_figure(self):
            global product_data

            # Count the number of products in each category
            category_count = {}
            for product in product_data:
                category = product.pro_category
                if category in category_count:
                    category_count[category] += 1
                else:
                    category_count[category] = 1

            # Sort the categories based on the count in descending order
            sorted_categories = sorted(category_count, key=lambda x: category_count[x], reverse=True)

            # Prepare the data for the bar chart
            categories = [category for category in sorted_categories]
            counts = [category_count[category] for category in sorted_categories]

            # Create the bar chart
            plt.bar(categories, counts)
            plt.xlabel('Category')
            plt.ylabel('Number of Products')
            plt.title('Product Count by Category')

            # Save the figure to the data/figure folder
            figure_path = 'data/figure/category_figure.png'
            os.makedirs(os.path.dirname(figure_path), exist_ok=True)
            plt.savefig(figure_path)
            plt.close()

        def generate_discount_figure(self):
            global product_data

            # Count the number of products in each discount range
            discount_ranges = {'Less than 30%': 0, '30% to 60%': 0, 'Greater than 60%': 0}
            for product in product_data:
                discount = product.pro_discount
                if discount < 30:
                    discount_ranges['Less than 30%'] += 1
                elif discount >= 30 and discount <= 60:
                    discount_ranges['30% to 60%'] += 1
                else:
                    discount_ranges['Greater than 60%'] += 1

            # Prepare the data for the pie chart
            labels = list(discount_ranges.keys())
            counts = list(discount_ranges.values())

            # Create the pie chart
            plt.pie(counts, labels=labels, autopct='%1.1f%%')
            plt.title('Product Discount Distribution')

            # Save the figure to the data/figure folder
            figure_path = 'data/figure/discount_figure.png'
            os.makedirs(os.path.dirname(figure_path), exist_ok=True)
            plt.savefig(figure_path)
            plt.close()

        def delete_all_products(self):
            # Clear the product_data list
            global product_data
            product_data.clear()

            # Remove the data/products.txt file
            import os
            os.remove('data/products.txt')

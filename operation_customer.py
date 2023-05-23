from datetime import time
import time


from model_customer import Customer
from operation_user import UserOperation


class CustomerOperation(UserOperation):
    loggedUser = ""
    customerId =0
    def get_profile(self):
        for customer in self.registered_customers:
            if customer.user_name == self.loggedUser:
                return customer

        return None



    def validate_email(self, user_email):
        # Email format validation logic
        if "@" in user_email and "." in user_email:
            username, domain = user_email.split("@")
            if len(username) > 0 and len(domain) > 0:
                domain_parts = domain.split(".")
                if len(domain_parts) > 1:
                    return True
        return False


    def validate_mobile(self, user_mobile):
        # Mobile number format validation logic
        if len(user_mobile) == 10 and user_mobile.isdigit():
            if user_mobile.startswith("04") or user_mobile.startswith("03"):
                return True
        return False

    def register_customer(self, user_name, user_password, user_email, user_mobile):
        # Validate the input values
        if not self.validate_username(user_name):
            return False,"User Name"

        if not self.validate_password(user_password):
            return False,"Unsafe Password"

        if not self.validate_email(user_email):
            return False,"User Email"

        if not self.validate_mobile(user_mobile):
            return False,"User Mobile"

        # Check if the user_name already exists
        for customer in self.registered_customers:
            if customer.user_name == user_name:
                return False,"Already Exists"

        # Generate a unique user_id
        user_id = self.generate_unique_user_id()

        # Get the current register time
        register_time = time.strftime("%d-%m-%Y_%H:%M:%S")

        user_password=self.encrypt_password(user_password)#encrypt the password before saving

        # Create a new Customer object
        new_customer = Customer(user_id, user_name, user_password, register_time, "customer", user_email, user_mobile)

        # Append the new_customer to registered_customers list
        self.registered_customers.append(new_customer)
        self.customer_list.append(new_customer)

        # Save the customer info into the data/users.txt file
        with open('data/users.txt', 'a') as file:
            file.write(str(new_customer) + "\n")

        return True,None

    def update_profile(self, attribute_name, value, customer_object):
        # Validate the attribute_name and value
        if attribute_name == 'user_name':
            if not UserOperation.validate_username(value):
                return False
        elif attribute_name == 'user_password':
            if not UserOperation.validate_password(value):
                return False
        elif attribute_name == 'user_email':
            if not self.validate_email(value):
                return False
        elif attribute_name == 'user_mobile':
            if not self.validate_mobile(value):
                return False

        # Update the customer object's attribute value
        setattr(customer_object, attribute_name, value)

        # Update the changes in the data/users.txt file
        with open('data/users.txt', 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if line.strip().startswith("{'user_id':'" + customer_object.user_id):
                    file.write(str(customer_object) + "\n")
                else:
                    file.write(line)
            file.truncate()

        return True

    def delete_customer(self, customer_id):
        # Read the existing customers from the file


        # Find the customer with the provided customer_id
        for customer in self.registered_customers:
            if customer.user_id == customer_id:
                # Remove the customer from the list
                self.registered_customers.remove(customer)
                self.customer_list.remove(customer)

                # Write the updated list of customers back to the file
                with open('data/users.txt', 'w') as file:
                    for customer in self.registered_customers:
                        file.write(str(customer) + "\n")

                return True

        return False

    def get_customer_list(self, page_number):

        # Calculate the total number of pages based on the number of customers and the maximum customers per page
        total_customers = len(self.registered_customers)
        max_customers_per_page = 10
        total_pages = (total_customers // max_customers_per_page) + (
            1 if total_customers % max_customers_per_page != 0 else 0)

        # Calculate the start and end indices for the given page number
        start_index = (page_number - 1) * max_customers_per_page
        end_index = start_index + max_customers_per_page

        # Retrieve the customers for the given page number
        customers = self.registered_customers[start_index:end_index]

        return customers, page_number, total_pages

    def delete_all_customers(self):
        global registered_customers

        # Clear the list of registered users
        registered_customers.clear()

        # Clear the contents of the data/users.txt file
        with open('data/users.txt', 'w') as file:
            file.write("")

        # Return None as there is no explicit return value
        return None

    def load_registered_customers(self):

        self.registered_customers.clear()  # Clear the existing customer data

        with open('data/users.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                customer_data = eval(line.strip())  # Convert the line string to a dictionary
                customer = Customer(
                    customer_data['user_id'],
                    customer_data['user_name'],
                    customer_data['user_password'],
                    customer_data['user_register_time'],
                    customer_data['user_role'],
                    customer_data['user_email'],
                    customer_data['user_mobile']
                )
                self.registered_customers.append(customer)
                self.customer_list.append(customer)
        return  self.registered_customers

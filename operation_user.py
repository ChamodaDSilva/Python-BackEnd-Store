import random
import re
import string

from operation_order import OrderOperation

class  UserOperation(OrderOperation):
    registered_customers = []  # Replace [...] with your actual implementation
    registered_admins = []  # Replace [...] with your actual implementation

    def generate_unique_user_id(self):
        prefix = 'u_'
        digits = ''.join(str(random.randint(0, 9)) for _ in range(10))
        user_id = prefix + digits
        return user_id

    def encrypt_password(self,user_password):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=len(user_password) * 2))
        encrypted_password = "^^"

        for i, char in enumerate(user_password):
            encrypted_password += random_string[i * 2:i * 2 + 2] + char

        encrypted_password += "$$"
        return encrypted_password

    def decrypt_password(self,encrypted_password):
        decrypted_password = ""

        # Removing the leading "^^" and trailing "$$"
        encrypted_password = encrypted_password[2:-2]

        # Iterating over the encrypted password in steps of 3
        for i in range(0, len(encrypted_password), 3):
            # Extracting two characters from the encrypted password
            random_chars = encrypted_password[i:i + 2]
            # Extracting one character from the encrypted password
            password_char = encrypted_password[i + 2]
            # Appending the password character to the decrypted password
            decrypted_password += password_char

        return decrypted_password

    def check_username_exist(self, user_name):

        # Check if the username exists in the registered users list
        if user_name in self.registered_customers:
            return True
        else:
            return False

    def validate_username(self, user_name):
        # Regular expression pattern to match letters and underscores
        pattern = r'^[a-zA-Z_]+$'

        # Check if the username matches the pattern and has a minimum length of 5 characters
        if re.match(pattern, user_name) and len(user_name) >= 5:
            return True
        else:
            return False

    def validate_password(self, user_password):
        # Regular expression pattern to match at least one letter (uppercase or lowercase) and one number
        pattern = r'^(?=.*[a-zA-Z])(?=.*\d).{5,}$'

        # Check if the password matches the pattern
        if re.match(pattern, user_password):
            return True
        else:
            return False

    def login(self, user_name, user_password):
        # Check if the provided user name and password combination matches a customer
        if len(self.registered_customers) != 0:
            for customer in self.registered_customers:
                if customer.user_name == user_name and self.decrypt_password(customer.user_password) == user_password:
                    return customer



        # Check if the provided user name and password combination matches an admin
        for admin in self.registered_admins:
            if admin.user_name == user_name and self.decrypt_password(admin.user_password) == user_password:
                return admin

        # If no matching customer or admin found, return None
        return None
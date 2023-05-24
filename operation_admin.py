import ast

from model_admin import Admin
from operation_customer import CustomerOperation


class AdminOperation(CustomerOperation):
    def register_admin(self):

        # # Check if an admin account already exists
        # if self.registered_admins:
        #     print("Admin account already registered.")
        #     return

        # Prompt for admin details
        print("--Admin Register--")
        has_admin = input("Do you have a admin account(yes/no): ")
        if has_admin == "yes":
            return
        admin_name = input("Enter admin user name: ")
        admin_password = input("Enter admin password: ")

        for admin in self.registered_admins:
            if admin.user_name== admin_name:
                print("Already Registered.")


        admin_password = self.encrypt_password(admin_password)

        # Create a new admin object
        admin = Admin(0, admin_name, admin_password)

        # Save the admin object to the list of registered admins
        self.registered_admins.append(admin)

        # Write the updated list of admins to the file
        with open('data/admins.txt', 'w') as file:
            for admin in self.registered_admins:
                file.write(str(admin) + "\n")

        print("Admin account registered successfully.")

    def load_all_admins(self):
        # Read the admin data from the file and create admin objects

        with open('data/admins.txt', 'r') as file:
            for line in file:
                admin_data = ast.literal_eval(line.strip())
                # Create an Admin object based on the admin_data and add it to the list
                admin = Admin(admin_data['user_id'], admin_data['user_name'], admin_data['user_password'],
                              admin_data['user_register_time'])
                self.registered_admins.append(admin)

        return self.registered_admins

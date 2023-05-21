from model_admin import Admin
from operation_customer import  CustomerOperation


class AdminOperation(CustomerOperation):
    def register_admin(self):

        # Check if an admin account already exists
        if self.registered_admins:
            print("Admin account already registered.")
            return

        # Prompt for admin details
        admin_name = "1"#input("Enter admin name: ")
        admin_password = "2"#input("Enter admin password: ")
        admin_password=self.encrypt_password(admin_password)

        # Create a new admin object
        admin = Admin(0,admin_name, admin_password)

        # Save the admin object to the list of registered admins
        self.registered_admins.append(admin)

        # Write the updated list of admins to the file
        with open('data/admins.txt', 'w') as file:
            for admin in self.registered_admins:
                file.write(str(admin) + "\n")

        print("Admin account registered successfully.")

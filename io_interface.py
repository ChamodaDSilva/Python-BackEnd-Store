class IOInterface:
    @staticmethod
    def get_user_input(message, num_of_args):
        user_input = input(message)
        args = user_input.split(" ")
        result = args[:num_of_args]
        result.extend([""] * (num_of_args - len(args)))
        return result

    @staticmethod
    def main_menu():
        print("Login Menu:")
        print("1. Login")
        print("2. Register")
        print("3. Quit")

        choice = input("Enter your choice: ")
        return choice

    @staticmethod
    def admin_menu():
        print("Admin Menu:")
        print("1. Show products")
        print("2. Add customers")
        print("3. Show customers")
        print("4. Show orders")
        print("5. Generate test data")
        print("6. Generate all statistical figures")
        print("7. Delete all data")
        print("8. Logout")

        choice = input("Enter your choice: ")
        return choice

    @staticmethod
    def customer_menu():
        print("Customer Menu:")
        print("1. Show profile")
        print("2. Update profile")
        print("3. Show products (e.g., '3 keyword' or '3')")
        print("4. Show history orders")
        print("5. Generate all consumption figures")
        print("6. Logout")

        choice = input("Enter your choice: ")
        return choice

    @staticmethod
    def show_list(user_role, list_type, object_list):
        if user_role == "customer" and list_type == "Customer":
            print("Access denied. You do not have permission to view customer list.")
        else:
            print(f"{list_type} List:")
            objects = object_list[0]
            page_number = object_list[1]
            total_page = object_list[2]

            for i, obj in enumerate(objects, start=1):
                print(f"{i}. {obj}")

            print(f"Page: {page_number}/{total_page}")

    @staticmethod
    def print_error_message(error_source, error_message):
        print(f"Error in {error_source}: {error_message}")

    @staticmethod
    def print_message(message):
        print(message)

    @staticmethod
    def print_object(target_object):
        print(str(target_object))

    @staticmethod
    def print_object_normal(objects):
        for i, obj in enumerate(objects, start=1):
            print(f"{i}. {obj}")
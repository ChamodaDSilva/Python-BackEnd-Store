from operation_user import UserOperation
from operation_admin import AdminOperation
from operation_customer import CustomerOperation
from opreation_product import ProductOperation
from io_interface import IOInterface


def main():
    interface = IOInterface()
    user_operation = UserOperation()
    admin_operation = AdminOperation()
    product_operation = ProductOperation()
    customer_operation = CustomerOperation()
    admin_operation.register_admin()


    admin_operation.load_registered_customers()
    #product_operation.extract_products_from_files()


    while True:
        interface.print_message("Welcome to the Online Store Management System!")
        interface.print_message("Please select an option:")
        interface.print_message("1. Login")
        interface.print_message("2. Register")
        interface.print_message("3. Quit")

        choice = interface.get_user_input("Enter your choice:", 1)[0]

        if choice == "1":
            username, password = interface.get_user_input("Enter your username and password:", 2)
            user = admin_operation.login(username, password)

            if user is not None:
                if user.user_role == "admin":
                    admin_menu(product_operation,admin_operation, interface)
                elif user.user_role == "customer":
                    admin_operation.loggedUser=username
                    customer_menu(admin_operation, interface)
            else:
                interface.print_error_message("UserOperation.login", "Username or password incorrect")

        elif choice == "2":
            username = interface.get_user_input("Enter the customer's username :", 1)[0]
            password = interface.get_user_input("Enter the user password:", 1)[0]
            userEmail = interface.get_user_input("Enter the user email:", 1)[0]
            userMobile = interface.get_user_input("Enter the user mobile:", 1)[0]

            success, err = admin_operation.register_customer(username, password, userEmail, userMobile)
            if not success:
                interface.print_error_message("Validation Error", err)
            else:
                interface.print_message("Customer added successfully!")

        elif choice == "3":
            interface.print_message("Thank you for using the Online Store Management System!")
            break

        else:
            interface.print_error_message("Main Menu", "Invalid choice. Please try again.")


def admin_menu(product_operation,admin_operation, interface):
    while True:
        interface.print_message("Admin Menu:")
        interface.print_message("1. Show products")
        interface.print_message("2. Add customers")
        interface.print_message("3. Show customers")
        interface.print_message("4. Show orders")
        interface.print_message("5. Generate test data")
        interface.print_message("6. Generate all statistical figures")
        interface.print_message("7. Delete all data")
        interface.print_message("8. Logout")

        choice = interface.get_user_input("Enter your choice:", 1)[0]

        if choice == "1":
            products = product_operation.get_product_list(1)
            show_list("admin", "Product", products, interface)

        elif choice == "2":
            username = interface.get_user_input("Enter the customer's username :", 1)[0]
            password=interface.get_user_input("Enter the user password:",1)[0]
            userEmail =interface.get_user_input("Enter the user email:",1)[0]
            userMobile = interface.get_user_input("Enter the user mobile:",1)[0]

            success,err=admin_operation.register_customer(username, password, userEmail, userMobile)
            if not success:
                interface.print_error_message("Validation Error",err)
            else:
                interface.print_message("Customer added successfully!")

        elif choice == "3":
            customers = admin_operation.get_customer_list(1)
            show_list("admin", "Customer", customers, interface)

        elif choice == "4":
            orders = admin_operation.get_order_list()
            show_list("admin", "Order", orders, interface)

        elif choice == "5":
            admin_operation.generate_test_data()
            interface.print_message("Test data generated successfully!")

        elif choice == "6":
            admin_operation.generate_all_statistical_figures()
            interface.print_message("All statistical figures generated successfully!")

        elif choice == "7":
            admin_operation.delete_all_data()
            interface.print_message("All data deleted successfully!")

        elif choice == "8":
            interface.print_message("Logged out successfully!")
            break

        else:
            interface.print_error_message("Admin Menu", "Invalid choice. Please try again.")


def customer_menu(admin_operation, interface):
    while True:
        interface.print_message("Customer Menu:")
        interface.print_message("1. Show profile")
        interface.print_message("2. Update profile")
        interface.print_message("3. Show products")
        interface.print_message("4. Show history orders")
        interface.print_message("5. Generate all consumption figures")
        interface.print_message("6. Logout")

        choice = interface.get_user_input("Enter your choice:", 1)[0]

        if choice == "1":
            profile = admin_operation.get_profile()
            if profile is None:
                interface.print_error_message("Customer Profile", "Empty")
            else:
                interface.print_object(profile)

        elif choice == "2":
            profile = admin_operation.get_profile()
            if profile is None:
                interface.print_error_message("Customer Profile", "Empty")
            else:
                interface.print_object(profile)
            attribute,name = interface.get_user_input("Enter your attribute name & new one:", 2)
            if admin_operation.update_profile(attribute,name,profile):
                interface.print_message("Profile updated successfully!")
            else:
                interface.print_error_message("Customer Update", "Validation Error")

        elif choice == "3":
            keyword = \
            interface.get_user_input("Enter a keyword to search for products (leave blank for all products):", 1)[0]
            products = admin_operation.get_product_list(keyword)
            show_list("customer", "Product", products, interface)

        elif choice == "4":
            orders = admin_operation.get_history_orders()
            show_list("customer", "Order", orders, interface)

        elif choice == "5":
            admin_operation.generate_all_consumption_figures()
            interface.print_message("All consumption figures generated successfully!")

        elif choice == "6":
            interface.print_message("Logged out successfully!")
            break

        else:
            interface.print_error_message("Customer Menu", "Invalid choice. Please try again.")


def show_list(user_role, list_type, object_list, interface):
    if user_role == "admin" or list_type != "Customer":
        page_number = object_list[1]
        total_pages = object_list[2]
        object_list = object_list[0]

        interface.print_message(f"{list_type} List:")
        for i, obj in enumerate(object_list, start=1):
            interface.print_message(f"Row {i}:")
            interface.print_object(obj)
            interface.print_message("")

        interface.print_message(f"Page Number: {page_number}/{total_pages}")
    else:
        interface.print_error_message("Show List", "Access denied")


if __name__ == "__main__":
    main()
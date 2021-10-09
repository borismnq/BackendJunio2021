from utils import Menu
from models import User, Assistance, Report


home_options = ["User", "Assistance", "Report"]
user_options = ["Add User", "Search User", "Remove User", "List Users"]
assistance_options = ["Checkin", "Checkout"]
report_options = ["User report", "Date report"]
home_menu = Menu("home", home_options)
user_menu = Menu("user", user_options)
assistance_menu = Menu("assistance", assistance_options)
report_menu = Menu("report", report_options)
show_home_menu = True


while show_home_menu:
    home_choice = home_menu.show()
    if home_choice == "0":
        show_home_menu = False
    elif home_choice == "1":
        show_user_menu = True
        while show_user_menu:
            user_choice = user_menu.show()
            if user_choice == "0":
                show_user_menu = False
            elif user_choice == "1":
                user_name = input("Insert user name: ")
                user_last_name = input("Insert user last name: ")
                user_dni = input("Insert user DNI: ")
                user_code = input("Insert user code: ")
                params = {
                    "name": user_name,
                    "last_name": user_last_name,
                    "code": user_code,
                    "dni": user_dni,
                }
                new_user = User(**params)
                added = new_user.add_user()
                if not added:
                    print("User not added")
                print("User added")
                input("Press a key to return")
                continue
            elif user_choice == "2":
                user_code = input("Insert user code to search: ")
                if user_code:
                    user = User.get_user(user_code)
                    if user:
                        print(f"User found: {user}")
                    else:
                        print("User not found")
                else:
                    print("Please enter a valid user code")
                input("Press a key to return")
                continue
            elif user_choice == "3":
                user_code = input("Insert user code to remove: ")
                if user_code:
                    removed = User.remove_user(user_code)
                    if removed:
                        print(f"User removed")
                    else:
                        print("User not found")
                else:
                    print("Please enter a valid user code")
                input("Press a key to return")
                continue

            elif user_choice == "4":
                users = User.get_users()
                if users:
                    print("\nUsers:")
                    for user in users:
                        print(f"- {user}")

                else:
                    print("0 users registered, add at least before list them")
                input("\nPress a key to return")
                continue
    elif home_choice == "2":
        show_assistance_menu = True
        while show_assistance_menu:
            assistance_choice = assistance_menu.show()
            if assistance_choice == "0":
                show_assistance_menu = False
            elif assistance_choice == "1":
                user_code = input("Insert user code to checkin: ")
                if user_code:
                    assistance = Assistance(user_code=user_code)
                    assistance.save(_in=True)
                else:
                    print("Please enter a valid user code")
                input("Press a key to return")
                continue
            elif assistance_choice == "2":
                user_code = input("Insert user code to checkout: ")
                if user_code:
                    assistance = Assistance(user_code=user_code)
                    assistance.save(_out=True)
                else:
                    print("Please enter a valid user code")
                input("Press a key to return")
                continue
    elif home_choice == "3":
        show_report_menu = True
        while show_report_menu:
            report_choice = report_menu.show()
            if report_choice == "0":
                show_report_menu = False
            elif report_choice == "1":
                user_code = input("Insert user code to get report: ")
                if user_code:
                    Report.get_user_report(user_code)
                else:
                    print("Please enter a valid user code")
                input("Press a key to return")
                continue
            elif report_choice == "2":
                day = int(input("Insert valid day of month (1=1st, 29=29th):"))
                month = int(
                    input("Insert valid month of year (1=January, 12=December):")
                )
                year = int(input("Insert valid year (2020, 2021):"))
                if day and month and year:
                    Report.get_date_report(day, month, year)
                else:
                    print("Please enter valid data")
                input("Press a key to return")
                continue
exit()

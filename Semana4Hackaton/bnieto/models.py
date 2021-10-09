import datetime
from utils import FileManager

users_file_name = "users.csv"
assistance_file_name = "assistance.csv"
user_headers = ["name", "last_name", "dni", "code"]
assistance_headers = [
    "user_code",
    "user_name",
    "user_last_name",
    "user_dni",
    "start_date",
    "end_date",
]


class Report:
    def __init__(self):
        pass

    @staticmethod
    def get_user_report(user_code):
        response = True
        try:
            user = User.get_user(user_code)
            if user:
                user_assistances_obj = Assistance(user_code=user_code)
                user_assistances = user_assistances_obj.get_user_assistances(user_code)
                if user_assistances:
                    name = user.get("user_name")
                    last_name = user.get("user_last_name")
                    print(f"\nAssistences report for {name} {last_name}:")
                    print("  Date      -  Checkin  -  Checkout")
                    for assistance in user_assistances:
                        date = datetime.datetime.strptime(
                            assistance.get("start_date"), "%m/%d/%Y, %H:%M:%S"
                        ).date()
                        checked_in = (
                            "Checked" if assistance.get("start_date") else "Miss"
                        )
                        checked_out = (
                            "Checked" if assistance.get("end_date") else "Miss"
                        )
                        print(f"{date}  -  {checked_in}  -  {checked_out}")
            else:
                print("Error: USER NOT FOUND")
        except Exception as e:
            print(e)
            print("Something went wrong.")
        return response

    @staticmethod
    def get_date_report(day, month, year):
        response = True
        try:
            all_assistances = Assistance.get_all_assistances()
            if all_assistances:
                report_date = datetime.datetime(year, month, day).date()
                report_users = list()
                for row in all_assistances:
                    row_date = datetime.datetime.strptime(
                        row.get("start_date"), "%m/%d/%Y, %H:%M:%S"
                    ).date()
                    if row_date == report_date:
                        report_users.append(row)
                print(f"Report for {report_date}:")
                print("User          -  Checking  -  Checkout")
                for user in report_users:
                    checked_in = "Checked" if user.get("start_date") else "Miss"
                    checked_out = "Checked" if user.get("end_date") else "Miss"

                    print(
                        f'{user.get("user_name")} {user.get("user_last_name")}-  {checked_in} -  {checked_out}'
                    )
        except Exception as e:
            print(e)
            print("Something went wrong.")
        return response


class Assistance:
    def __init__(self, **kwargs):
        self.user_code = kwargs.get("user_code")
        self.user_name = kwargs.get("user_name")
        self.user_last_name = kwargs.get("user_last_name")
        self.user_dni = kwargs.get("user_dni")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")

    def save(self, _in=False, _out=False):
        response = False
        user = User.get_user(self.user_code)
        if user:
            try:
                file_manager = FileManager(assistance_file_name)
                user_assistences = self.get_user_assistances(self.user_code)
                current_user_assistance = self.get_current_user_assistance(
                    user_assistences
                )
                if current_user_assistance:
                    current_user_assistance_obj = Assistance(**current_user_assistance)
                    if not current_user_assistance_obj.is_user_full_checked():
                        if _out:
                            self.user_name = current_user_assistance_obj.user_name
                            self.user_last_name = (
                                current_user_assistance_obj.user_last_name
                            )
                            self.user_dni = current_user_assistance_obj.user_dni
                            self.start_date = current_user_assistance_obj.start_date
                            self.end_date = datetime.datetime.now().strftime(
                                "%m/%d/%Y, %H:%M:%S"
                            )
                            file_manager.update_row(
                                assistance_headers,
                                "user_code",
                                self.user_code,
                                self.__dict__,
                            )
                            print("CHECKOUT SAVED!")
                            response = True

                        else:
                            print("Error: This user is already checked in.")
                    else:
                        print("Error: Assistance already fullchecked for this user")
                else:
                    if _in:
                        self.start_date = datetime.datetime.now().strftime(
                            "%m/%d/%Y, %H:%M:%S"
                        )
                        self.user_name = user.get("name")
                        self.user_last_name = user.get("last_name")
                        self.user_dni = user.get("dni")
                        file_manager.write_as_csv(self.__dict__, assistance_headers)
                        print("CHECKIN SAVED!")
                        response = True
                    else:
                        print("Error: You can't checkout before checkin ")

            except Exception as e:
                print(e)
        else:
            print("Error: USER NOT FOUND")
        return response

    def is_user_full_checked(self):
        return True if (self.start_date and self.end_date) else False

    @staticmethod
    def get_all_assistances():
        response = list()
        try:
            file_manager = FileManager(assistance_file_name)
            response = file_manager.read_as_csv(headers=assistance_headers)
        except Exception as e:
            print(e)
        return response

    def get_user_assistances(self, user_code):
        user_assistances = list()
        try:
            file_manager = FileManager(assistance_file_name)
            all_data = file_manager.read_as_csv(headers=assistance_headers)
            for row in all_data:
                if row.get("user_code") == user_code:
                    user_assistances.append(row)
        except Exception as e:
            print(e)
        return user_assistances

    def get_current_user_assistance(self, user_assistances):
        response = None
        current_date = datetime.datetime.now().date()
        try:
            for user_assistance in user_assistances:
                start_date = datetime.datetime.strptime(
                    user_assistance.get("start_date"), "%m/%d/%Y, %H:%M:%S"
                )
                if current_date == start_date.date():
                    response = user_assistance
                    break
        except Exception as e:
            print(e)
        return response


class User:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.last_name = kwargs.get("last_name")
        self.code = kwargs.get("code")
        self.dni = kwargs.get("dni")

    def add_user(self):
        response = False
        try:
            file_manager = FileManager(users_file_name)
            file_manager.write_as_csv(self.__dict__, user_headers)
            response = True
        except Exception as e:
            print(e)
        return response

    @staticmethod
    def get_users():
        response = None
        try:
            file_manager = FileManager(users_file_name)
            response = file_manager.read_as_csv()
        except Exception as e:
            print(e)
        return response

    @staticmethod
    def get_user(code):
        response = None
        query = ["code", code]
        try:
            file_manager = FileManager(users_file_name)
            response = file_manager.get_row(query[0], query[1])
        except Exception as e:
            print(e)
        return response

    @staticmethod
    def remove_user(code):
        response = False
        query = ["code", code]
        try:
            file_manager = FileManager(users_file_name)
            response = file_manager.remove_row(user_headers, query[0], query[1])
        except Exception as e:
            print(e)
        return response

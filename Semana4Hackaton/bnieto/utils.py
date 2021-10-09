import os
import csv
import shutil
import time

from tempfile import NamedTemporaryFile


class Menu:
    def __init__(self, name, options_list):
        options_list.append("Exit")
        self.options_list = options_list
        self.menu_name = name

    def show(self):
        while True:
            self.limpiarPantalla()
            print("======" + self.menu_name.upper() + " MENU ======\n")
            for index, value in enumerate(self.options_list):
                print(
                    str(index + 1 if value != self.options_list[-1] else "0")
                    + " → "
                    + value
                )
            print("\n")
            answer = input("Please select an option:")
            if answer in [
                str(index + 1 if value != self.options_list[-1] else "0")
                for index, value in enumerate(self.options_list)
            ]:
                if answer.upper() == "0":
                    print("Bye.")
                break
            else:
                print("Opción no valida, escoja una opción valida")
                time.sleep(1)
        return answer

    def limpiarPantalla(self):
        def clear():
            return os.system("clear")

        clear()


class FileManager:
    def __init__(self, filename):
        self.filename = filename
        self.current_path = os.getcwd()
        self.filepath = self.current_path + "/" + self.filename

    def update_path(self, path):
        self.current_path = path
        self.filepath = self.current_path + "/" + self.filename

    def read(self):
        try:
            opened_file = open(self.filepath, "r")
            return opened_file.read()
        except Exception as e:
            print(e)
        finally:
            opened_file.close()

    def create_csv_file_with_headers(self, headers):
        response = False
        path = self.filepath
        if not os.path.isfile(path):
            opened_file = open(path, "w", newline="")
            opened_file.close()
            opened_file = open(path, "a", newline="")
            writer = csv.DictWriter(opened_file, fieldnames=headers)
            writer.writeheader()
            response = True
        return response

    def read_as_csv(self, headers=None):
        response = None
        try:
            opened_file = open(self.filepath, newline="")
            # opened_file = open(self.filepath, newline='')
            response = csv.DictReader(opened_file, delimiter=",")
        except FileNotFoundError as e:
            print("File not found, creating it ...")
            is_file_created = self.create_csv_file_with_headers(headers)
            if is_file_created:
                opened_file = open(self.filepath, newline="")
                response = csv.DictReader(opened_file, delimiter=",")
        except Exception as e:
            print(e)
        return response

    def write_as_csv(self, data_dict, headers):
        try:
            path = self.filepath

            if os.path.isfile(path):
                try:
                    opened_file = open(self.filepath, "a", newline="")
                    writer = csv.DictWriter(opened_file, fieldnames=headers)
                    writer.writerow(data_dict)
                    print(f"Row added {data_dict}")
                except Exception as e:
                    print(e)
                finally:
                    opened_file.close()
            else:
                opened_file = open(self.filepath, "w", newline="")
                opened_file.close()
                opened_file = open(self.filepath, "a", newline="")
                writer = csv.DictWriter(opened_file, fieldnames=headers)
                writer.writeheader()
                writer.writerow(data_dict)

        except Exception as write_error:
            print(write_error)

    def get_row(self, identifier_name, identifier_value):

        try:
            path = self.filepath
            with open(path, "r") as csvfile:
                file_reader = csv.DictReader(csvfile, delimiter=",")
                for row in file_reader:
                    if row.get(identifier_name) == identifier_value:
                        return row
        except Exception as e:
            print(e)

    def remove_row(self, headers, identifier_name, identifier_value):
        response = False
        try:
            path = self.filepath
            tempfile = NamedTemporaryFile(mode="w", delete=False)
            with open(path, "r") as csvfile, tempfile:
                file_reader = csv.DictReader(csvfile, delimiter=",")
                file_writer = csv.DictWriter(tempfile, fieldnames=headers)
                file_writer.writeheader()
                for row in file_reader:
                    if row.get(identifier_name) == identifier_value:
                        print(f"Removing row with {identifier_name}={identifier_value}")
                        response = True
                    else:
                        file_writer.writerow(row)
            shutil.move(tempfile.name, path)
        except Exception as e:
            print(e)
        return response

    def update_row(self, headers, identifier_name, identifier_value, updated_row):

        try:
            path = self.filepath
            tempfile = NamedTemporaryFile(mode="w", delete=False)
            with open(path, "r") as csvfile, tempfile:
                file_reader = csv.DictReader(csvfile, delimiter=",")
                file_writer = csv.DictWriter(tempfile, fieldnames=headers)
                file_writer.writeheader()
                for row in file_reader:
                    if row.get(identifier_name) == identifier_value:
                        print(f"Updating row with {identifier_name}={identifier_value}")
                        file_writer.writerow(updated_row)
                    else:
                        file_writer.writerow(row)
            shutil.move(tempfile.name, path)
        except Exception as e:
            print(e)

    def remove_file(self):
        path = self.filepath
        if os.path.isfile(path):
            try:
                os.remove(path)
                print(f"File {self.filepath} was successfully removed")
            except Exception as error:
                print(error)

    def write(self, row):
        try:
            path = self.filepath
            if os.path.isfile(path):
                try:
                    opened_file = open(self.filepath, "a")
                    opened_file.write(row + "\n")
                except Exception as e:
                    print(e)
                finally:
                    opened_file.close()
            else:
                opened_file = open(self.filepath, "w")
                opened_file.close()
                opened_file = open(self.filepath, "a")
                opened_file.write(row + "\n")
        except Exception as write_error:
            print(write_error)

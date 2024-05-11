from PyQt6.QtWidgets import *
from gui import *
import csv
import os.path


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        Logic.file_name = ''

        self.shrink_screen()
        self.button_modify.hide()
        self.button_delete.hide()
        self.calendar.clicked.connect(lambda: self.change_date_label())
        self.button_add_event.clicked.connect(lambda: self.expand_screen())
        self.button_add_event.clicked.connect(lambda: self.change_date_label())
        self.button_cancel.clicked.connect(lambda: self.shrink_screen())
        self.button_cancel.clicked.connect(lambda: self.clear())
        self.radioButton_yes.clicked.connect(lambda: self.all_day())
        self.radioButton_no.clicked.connect(lambda: self.all_day())
        self.button_confirm.clicked.connect((lambda: self.confirm()))
        self.list_events.itemClicked.connect(self.view_item)
        self.button_modify.clicked.connect((lambda: self.modify()))
        self.button_delete.clicked.connect(lambda: self.delete())

    def shrink_screen(self):
        try:
            self.setMinimumSize(QtCore.QSize(810, 470))
            self.setMaximumSize(QtCore.QSize(810, 470))
        except Exception as e:
            print(f"{e}")

    def expand_screen(self):
        self.setMaximumSize(QtCore.QSize(810, 810))
        self.setMinimumSize(QtCore.QSize(810, 810))
        self.hide_time()

    def hide_time(self):
        self.label_start.hide()
        self.label_end.hide()
        self.timeEdit_start.hide()
        self.timeEdit_end.hide()

    def show_time(self):
        self.label_start.show()
        self.label_end.show()
        self.timeEdit_end.show()
        self.timeEdit_start.show()

    def change_date(self):
        month = self.calendar.selectedDate().month()
        year = self.calendar.selectedDate().year()
        day = self.calendar.selectedDate().day()

        return month, day, year

    def get_month(self, month):
        month = str(month)
        if month == '1' or month == '01':
            return 'January'
        elif month == '2' or month == '02':
            return 'February'
        elif month == '3' or month == '03':
            return 'March'
        elif month == '4' or month == '04':
            return 'April'
        elif month == '5' or month == '05':
            return 'May'
        elif month == '6' or month == '06':
            return 'June'
        elif month == '7' or month == '07':
            return 'July'
        elif month == '8' or month == '08':
            return 'August'
        elif month == '9' or month == '09':
            return 'September'
        elif month == '10':
            return 'October'
        elif month == '11':
            return 'November'
        elif month == '12':
            return 'December'

    def numeric_date(self):
        return self.calendar.selectedDate().toPyDate()

    def change_date_label(self):
        month, day, year = self.change_date()
        month = self.get_month(month)
        self.label_date.setText(f'{month} {day}, {year}')

    def confirm(self):
        try:
            title = self.input_title.text().strip()
            location = self.input_location.text()

            start_time = self.timeEdit_start.time().toString("hh:mm ap")
            end_time = self.timeEdit_end.time().toString("hh:mm ap")

            exact_start_time = self.timeEdit_start.time().msecsSinceStartOfDay()
            exact_end_time = self.timeEdit_end.time().msecsSinceStartOfDay()

            if title == '':
                raise ValueError('Please enter in a title.')
            elif location == '':
                raise ValueError('Please enter in a location.')

            if self.radioButton_no.isChecked():
                if exact_start_time >= exact_end_time:
                    print(exact_start_time)
                    print(exact_end_time)
                    raise ValueError('The start time cannot be the same or later than the end time.')
            elif self.radioButton_yes.isChecked():
                start_time = '12:00 am'
                end_time = '12:00 pm'
            else:
                raise ValueError('Please state whether it is an all-day event or not')

        except ValueError as e:
            self.label_handling.setText(f'{e}')
        except Exception as e:
            print(f'{e}')
        else:
            self.clear()
            self.shrink_screen()
            self.create_date(self.numeric_date(), title, location, start_time, end_time)

    def all_day(self):
        if self.radioButton_yes.isChecked():
            self.hide_time()
        elif self.radioButton_no.isChecked():
            self.show_time()

    def clear(self):
        try:
            self.input_title.clear()
            self.input_location.clear()
            self.buttonGroup.setExclusive(False)
            self.radioButton_yes.setChecked(False)
            self.radioButton_no.setChecked(False)
            self.buttonGroup.setExclusive(True)
            self.calendar.setDisabled(False)
            self.button_add_event.setDisabled(False)
            self.label_handling.setText('')
            self.button_confirm.show()
            self.button_modify.hide()
            self.button_delete.hide()
            self.input_title.show()
            self.input_location.show()
            self.label_allday.show()
            self.radioButton_yes.show()
            self.radioButton_no.show()
            self.label_start.hide()
            self.label_end.hide()
            self.label_event_title.setText("Title of Event: ")
            self.label_location.setText('Location: ')
            self.label_start.setText('Start: ')
            self.label_end.setText('End: ')
        except Exception as e:
            print(f'{e}')

        Logic.file_name = ''

    def toggle_event(self):
        self.expand_screen()
        self.button_confirm.hide()
        self.button_modify.show()
        self.button_delete.show()
        self.input_title.hide()
        self.input_location.hide()
        self.label_allday.hide()
        self.radioButton_yes.hide()
        self.radioButton_no.hide()
        self.label_start.show()
        self.label_end.show()


    def create_date(self, numeric_date, title, location, start_time, end_time):
        try:
            flag = 0
            file_name = str(numeric_date) + '_' + title.replace(' ', '_')
            print(file_name)
            information = [str(numeric_date), title, location, start_time, end_time]
            with open(file_name + '.csv', 'w') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(information)

            testing_file = file_name.replace('_', ' ')
            print(testing_file)
            for index in range(self.list_events.count()):
                item = self.list_events.item(index)
                print(item.text())
                if item.text() == (testing_file):
                    flag = 1

            if flag == 0:
                self.list_events.addItem(f'{numeric_date} {title}')
                self.list_events.sortItems()

            Logic.file_name = file_name + '.csv'
        except Exception as e:
            print(f'{e}')

    def view_item(self, item):
        try:
            file_name = item.text().split()
            file_name = '_'.join(file_name) + '.csv'
            with open(file_name, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                line = next(csv_reader)

            self.toggle_event()
            self.calendar.setDisabled(True)
            self.button_add_event.setDisabled(True)

            self.label_event_title.setText(f"Title of Event: \t{line[1]}")
            self.label_location.setText(f"Location: \t{line[2]}")
            self.label_start.setText(f"Start Time: \t{line[3]}")
            self.label_end.setText(f"End Time: \t{line[4]}")

            Logic.file_name = file_name
        except Exception as e:
            print(f'{e}')

    def modify(self):
        try:
            safety_file = Logic.file_name
            print(f"top logic: {Logic.file_name}")
            with open(Logic.file_name, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                line = next(csv_reader)

            self.clear()
            self.button_delete.show()
            self.label_date.setText(f'{self.get_month(line[0][5:7])} {line[0][:-2]}, {line[0][0:4]}')
            self.input_title.setText(f'{line[1]}')
            self.input_location.setText(f'{line[2]}')
            if line[3] == "12:00 am" and line[4] == "12:00 pm":
                self.radioButton_yes.setChecked(True)
            else:
                self.radioButton_no.setChecked(True)
                self.show_time()

            Logic.file_name = safety_file
            self.button_modify.hide()
        except Exception as e:
            print(f'{e}')

    def delete(self):
        try:
            if os.path.exists(Logic.file_name):
                os.remove(Logic.file_name)
            first_half = Logic.file_name.replace('_', ' ')[:10]
            second_half = Logic.file_name.replace('_', ' ')[11:-4]
            for index in range(self.list_events.count()):
                item = self.list_events.item(index)
                if item.text() == (first_half + ' ' + second_half):
                    self.list_events.takeItem(index)
            self.clear()
            self.shrink_screen()
        except Exception as e:
            print(f'{e}')
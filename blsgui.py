import pymysql
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from typing import *


class DBLoginDialog(QDialog):
    def __init__(self):
        super(DBLoginDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Login to MySQL Server")
        layout = QGridLayout()
        self.setLayout(layout)

        label = QLabel("MySQL Server Login Credentials")
        layout.addWidget(label, 0, 0)
        labelhost = QLabel("Host:")
        self.host = QLineEdit("localhost")
        labeluser = QLabel("User:")
        self.user = QLineEdit("root")
        labelpass = QLabel("Password:")
        self.password = QLineEdit()
        labeldata = QLabel("Database:")
        self.database = QLineEdit("blsqcew")
        layout.addWidget(labelhost, 1, 0)
        layout.addWidget(self.host, 1, 1)
        layout.addWidget(labeluser, 2, 0)
        layout.addWidget(self.user, 2, 1)
        layout.addWidget(labelpass, 3, 0)
        layout.addWidget(self.password, 3, 1)
        layout.addWidget(labeldata, 4, 0)
        layout.addWidget(self.database, 4, 1)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.rejectA)

        layout.addWidget(self.buttons)

    def accept(self):
        global connection
        try:
            connection = pymysql.connect(host=self.host.text(),
                                         user=self.user.text(),
                                         password=self.password.text(),
                                         db=self.database.text(),
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            print(f"Couldn't log {self.user.text()} in to MySQL server on {self.host.text()}")
            print(e)
            self.rejectA()

        self.reject()
        main = MainWindow()
        main.exec()

    def rejectA(self):
        qApp.quit()
        sys.exit()


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("BLSQCEW Database")
        layout = QGridLayout()
        self.setLayout(layout)

        label = QLabel("BLSQCEW Database GUI")
        layout.addWidget(label, 0, 0)
        labelY = QLabel("Year:")
        self.year = QComboBox()
        cursor = connection.cursor()
        cursor.execute("select distinct year from combined_annuals")
        years = cursor.fetchall()
        for year in years:
            self.year.addItem(f"{year['year']}")
        labelQ = QLabel("Quarter:")
        self.quarter = QComboBox()
        self.quarter.addItem("1")
        self.quarter.addItem("2")
        self.quarter.addItem("3")
        self.quarter.addItem("4")
        self.quarter.addItem("A")
        labelI = QLabel("Industry:")
        self.industry = QLineEdit("Total, all industries")
        self.industry.textChanged.connect(self.change)
        self.button = QPushButton("Search")
        self.button.clicked.connect(self.search)
        layout.addWidget(labelY, 1, 0)
        layout.addWidget(self.year, 1, 1)
        layout.addWidget(labelQ, 2, 0)
        layout.addWidget(self.quarter, 2, 1)
        layout.addWidget(labelI, 3, 0)
        layout.addWidget(self.industry, 3, 1)
        layout.addWidget(self.button, 4, 0, 1, 2)


    def search(self):
        cursor = connection.cursor()
        text = self.industry.text()
        cursor.execute("select distinct industry_title from industry_titles;")
        industries = cursor.fetchall()
        for industry in industries:
            if text == industry["industry_title"]:
                if self.quarter.currentText() == "A":
                    dataText = f"select * from combined_annuals join industry_titles on combined_annuals.industry_code = industry_titles.industry_code where combined_annuals.year = '{self.year.currentText()}' and industry_titles.industry_title = '{self.industry.text()}'"
                    cursor.execute(dataText)
                    data = cursor.fetchall()
                    self.reject()
                    dataTable = ShowSelectedData(data)
                    dataTable.exec()
                else:
                    dataText = f"select * from combined_quarters join industry_titles on combined_quarters.industry_code = industry_titles.industry_code where combined_quarters.year = '{self.year.currentText()}' and industry_titles.industry_title = '{self.industry.text()}' and combined_quarters.qtr = '{self.quarter.currentText()}'"
                    cursor.execute(dataText)
                    data = cursor.fetchall()
                    self.reject()
                    dataTable = ShowSelectedData(data)
                    dataTable.exec()
            else:
                QMessageBox.about(self, "Invalid", "You've entered an invalid industry")



    def change(self):
        if len(self.industry.text()) == 0:
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)


class SimpleTableModel(QAbstractTableModel):

    def __init__(self, data: List[Dict[str, str]]):
        QAbstractTableModel.__init__(self, None)
        self.data = data[:100]
        self.headers = [k for k, v in data[0].items()]
        self.rows = [[v for k, v in record.items()] for record in self.data]

    def rowCount(self, parent):
        return len(self.rows)

    def columnCount(self, parent):
        return len(self.headers)

    def data(self, index, role):
        if (not index.isValid()) or (role != Qt.DisplayRole):
            return QVariant()
        else:
            return QVariant(self.rows[index.row()][index.column()])

    def row(self, index):
        return self.data[index]

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        elif orientation == Qt.Vertical:
            return section + 1
        else:
            return self.headers[section]


class ShowSelectedData(QDialog):

    def __init__(self, data):
        super(ShowSelectedData, self).__init__()
        self.setWindowTitle("Selected Data")
        layout = QGridLayout()
        self.setLayout(layout)

        label = QLabel("Filter Selected Data")
        layout.addWidget(label, 0, 0)
        labelY = QLabel("Year:")
        self.year = QComboBox()
        cursor = connection.cursor()
        cursor.execute("select distinct year from combined_annuals")
        years = cursor.fetchall()
        for year in years:
            self.year.addItem(f"{year['year']}")
        labelQ = QLabel("Quarter:")
        self.quarter = QComboBox()
        self.quarter.addItem("1")
        self.quarter.addItem("2")
        self.quarter.addItem("3")
        self.quarter.addItem("4")
        self.quarter.addItem("A")
        labelI = QLabel("Industry:")
        self.industry = QLineEdit("Total, all industries")
        self.industry.textChanged.connect(self.change)
        labelO = QLabel("Order By:")
        self.order = QComboBox()
        self.order.addItem("None")
        self.order.addItem("total quarterly wages")
        self.order.addItem("average weekly wages")
        self.order.addItem("average annual pay")
        self.order.addItem("average annual weekly wages")
        self.button = QPushButton("Filter")
        self.button.clicked.connect(self.filter)
        layout.addWidget(labelY, 1, 0)
        layout.addWidget(self.year, 1, 1)
        layout.addWidget(labelQ, 2, 0)
        layout.addWidget(self.quarter, 2, 1)
        layout.addWidget(labelI, 3, 0)
        layout.addWidget(self.industry, 3, 1)
        layout.addWidget(labelO, 4, 0)
        layout.addWidget(self.order, 4, 1)
        layout.addWidget(self.button, 5, 0, 1, 2)

        try:
            self.table_model = SimpleTableModel(data)
            self.table_view = QTableView()
            self.table_view.setModel(self.table_model)
            self.table_view.setSelectionMode(QAbstractItemView.SelectRows | QAbstractItemView.SingleSelection)
            layout.addWidget(self.table_view, 6, 0, 1, 2)
            self.table_view.clicked.connect(self.enable_button)

        except IndexError:
            QMessageBox.about(self, "Empty Table", "The table is empty")

        self.buttonB = QPushButton("Back")
        self.buttonB.clicked.connect(self.back)
        layout.addWidget(self.buttonB, 7, 0, 1, 2)

        self.buttonDetail = QPushButton("Detail")
        self.buttonDetail.clicked.connect(self.detail)
        self.buttonDetail.setEnabled(False)
        layout.addWidget(self.buttonDetail, 8, 0, 1, 2)

    def change(self):
        if len(self.industry.text()) == 0:
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def filter(self):
        pass

    def back(self):
        self.close()
        main = MainWindow()
        main.exec()

    def enable_button(self):
        if self.table_view.currentIndex() == -1:
            self.buttonDetail.setEnabled(False)
        else:
            self.buttonDetail.setEnabled(True)

    def detail(self):
        current_index = self.table_view.currentIndex().row()
        selected_item = self.table_model.row(current_index)
        SelectedDataDetail(selected_item).exec()


class SelectedDataDetail(QDialog):
    def __init__(self, row):
        super(SelectedDataDetail, self).__init__()
        self.setWindowTitle("Selected Data Detail")
        group_box = QGroupBox()
        layout = QFormLayout()
        for key, value in row.items():
            layout.addRow(QLabel(str(key)), QLabel(str(value)))
        group_box.setLayout(layout)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(group_box)
        vbox_layout.addWidget(buttons)
        self.setLayout(vbox_layout)

    def accept(self):
        self.close()

if __name__=='__main__':
    app = QApplication(sys.argv)


    login = DBLoginDialog()
    login.exec()


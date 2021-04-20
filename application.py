# #################################################################
# File name:    application.py
# Author:       Zhangshun Lu
# Create on:    2021-04-20
# Description:  GUI application for managing the workshop inventory
# #################################################################

from PyQt5 import QtCore
import database_ee
import database_mech
import sqlite3
import sys
import os.path
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowIcon(QIcon("icon/lab.png"))
        self.setWindowTitle("Lab Inventory Management System")
        self.setMinimumSize(1200, 800)

        # -------------------------------- #
        #       Menubar and Toolbar        #
        # -------------------------------- #
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&About")

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # ========== Menubar ========== #
        add_item_action = QAction(QIcon("icon/add.png"), "Add new item", self)
        add_item_action.triggered.connect(self.insert)
        file_menu.addAction(add_item_action)

        search_item_action = QAction(
            QIcon("icon/search.png"), "Search Item", self)
        search_item_action.triggered.connect(self.search)
        file_menu.addAction(search_item_action)

        del_item_action = QAction(QIcon("icon/delete.png"), "Delete", self)
        del_item_action.triggered.connect(self.delete)
        file_menu.addAction(del_item_action)

        file_menu.addSeparator()

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.quit)
        file_menu.addAction(quit_action)

        about_action = QAction(QIcon("icon/information.png"), "Developer",
                               self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        # ========== Toolbar ========== #
        # Set toolbar spacing
        toolbar.setStyleSheet("QToolBar{spacing:10px;}")

        btn_add_item = QAction(QIcon("icon/add.png"), "Add new item",
                               self)
        btn_add_item.triggered.connect(self.insert)
        btn_add_item.setStatusTip("Add new item")
        toolbar.addAction(btn_add_item)

        btn_view_all = QAction(QIcon("icon/view.png"), "View all",
                               self)
        btn_view_all.triggered.connect(self.load_data)
        btn_view_all.setStatusTip("View all")
        toolbar.addAction(btn_view_all)

        btn_search_item = QAction(QIcon("icon/search.png"), "Search item",
                                  self)
        btn_search_item.triggered.connect(self.search)
        # btn_search_item.setShortcut("Ctrl+F")
        btn_search_item.setStatusTip("Search item")
        toolbar.addAction(btn_search_item)

        btn_delete_item = QAction(
            QIcon("icon/delete.png"), "Delete item", self)
        btn_delete_item.triggered.connect(self.delete)
        btn_delete_item.setStatusTip("Delete item")
        toolbar.addAction(btn_delete_item)

        btn_export = QAction(QIcon("icon/export.png"), "Export to CSV", self)
        btn_export.triggered.connect(self.export)
        btn_export.setStatusTip("Export to CSV")
        toolbar.addAction(btn_export)

        # ========== Button Widgets ========== #
        btn_add = QPushButton("Add", self)
        btn_add.clicked.connect(self.insert)
        btn_add.setIcon(QIcon("icon/add.png"))
        btn_add.setFixedWidth(100)
        btn_add.setFixedHeight(35)

        btn_clear = QPushButton("Clear", self)
        btn_clear.clicked.connect(self.clear)
        btn_clear.setIcon(QIcon("icon/clear.png"))
        btn_clear.setFixedWidth(100)
        btn_clear.setFixedHeight(35)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Type Item id.")
        self.search_box.setFixedWidth(100)
        self.search_box.setFixedHeight(20)

        btn_search = QPushButton("Search", self)
        btn_search.clicked.connect(self.search_item)
        btn_search.setIcon(QIcon("icon/search.png"))
        btn_search.setFixedWidth(100)
        btn_search.setFixedHeight(35)

        btn_delete = QPushButton("Delete", self)
        btn_delete.clicked.connect(self.delete)
        btn_delete.setIcon(QIcon("icon/delete.png"))
        btn_delete.setFixedWidth(100)
        btn_delete.setFixedHeight(35)

        btn_update = QPushButton("Update", self)
        btn_update.clicked.connect(self.update)
        btn_update.setIcon(QIcon("icon/update.png"))
        btn_update.setFixedWidth(100)
        btn_update.setFixedHeight(35)

        # ------------------------------- #
        #       Main Window Layout        #
        # ------------------------------- #
        layout = QGridLayout()
        layout_buttons = QVBoxLayout()

        self.main_window_widget = QWidget()
        self.main_window_widget.setLayout(layout)

        self.item_info_window = EntryWindow()

        self.key = self.item_info_window.pageCombo.activated.connect(
            self.select_table)

        self.table_title = QLabel("Inventory List")
        self.table_title.setFont(QFont("Arial", 14))

        self.tableWidget = QTableWidget()
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(10)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(
            ("Item id", "Description", "Manufacture Part No.", "Category",
             "Package", "Value", "Unit", "Cabinet", "Amount", "Notes"))
        self.tableWidget.setSortingEnabled(True)

        empty_widget = QLabel()
        empty_widget.setFixedSize(100, 55)
        layout_buttons.addWidget(empty_widget)
        layout_buttons.addWidget(btn_add)
        layout_sub_buttons = QVBoxLayout()
        layout_sub_buttons.addWidget(self.search_box)
        layout_sub_buttons.addWidget(btn_search)
        layout_sub_buttons.addWidget(btn_clear)
        layout_sub_buttons.addWidget(btn_delete)
        layout_sub_buttons.addWidget(btn_update)
        layout_buttons.addLayout(layout_sub_buttons)

        layout.addWidget(self.item_info_window, 0, 0, 1, 3)
        layout.addLayout(layout_buttons, 0, 3)
        layout.addWidget(self.table_title, 1, 0)
        layout.addWidget(self.tableWidget, 2, 0, 1, 4)

        self.setCentralWidget(self.main_window_widget)

        # ------------------------------- #
        #      Variables & Functions      #
        # ------------------------------- #
        self.conn = sqlite3.connect("inventory.db")
        self.result = []

    def load_data(self):
        if self.key == "ELECTRONICS":
            self.result = database_ee.show_table()
        elif self.key == "MECHANICS":
            self.tableWidget.setColumnCount(6)
            self.result = database_mech.show_table()
        self.display()

    def display(self):
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(self.result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                # format the cell information
                data = str(data)
                if "\n" in data:
                    data = data.replace("\n", "")
                else:
                    pass
                self.tableWidget.setItem(row_number, column_number,
                                         QTableWidgetItem(str(data)))
                self.tableWidget.resizeColumnToContents(0)
                self.tableWidget.resizeColumnToContents(2)
                self.tableWidget.resizeColumnsToContents()

    def select_table(self):
        self.key = self.item_info_window.pageCombo.currentText()
        if self.key == "ELECTRONICS":
            self.tableWidget.setColumnCount(10)
            self.tableWidget.setHorizontalHeaderLabels(
                ("Item id", "Description", "Manufacture Part No.", "Category",
                 "Package", "Value", "Unit", "Cabinet", "Amount", "Notes"))
        elif self.key == "MECHANICS":
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setHorizontalHeaderLabels(
                ("Item id", "Description", "Manufacture Part No.", "Category",
                 "Cabinet", "Amount", "Notes"))
        self.load_data()
        return self.key

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def insert(self):
        if self.key == "ELECTRONICS":
            description = self.item_info_window.description_ee.text()
            part_number = self.item_info_window.part_number_ee.text()
            category = self.item_info_window.category_ee.itemText(
                self.item_info_window.category_ee.currentIndex())
            package = self.item_info_window.package_ee.text()
            value = self.item_info_window.value_ee.text()
            unit = self.item_info_window.unit_ee.itemText(
                self.item_info_window.unit_ee.currentIndex())
            cabinet = self.item_info_window.cabinet_ee.text()
            amount = self.item_info_window.amount_ee.text()
            notes = self.item_info_window.notes_ee.text()
            database_ee.add_row(description, part_number, category,
                                package, value, unit, cabinet, amount, notes)
        elif self.key == "MECHANICS":
            description = self.item_info_window.description_mech.text()
            part_number = self.item_info_window.part_number_mech.text()
            category = self.item_info_window.category_mech.itemText(
                self.item_info_window.category_mech.currentIndex())
            cabinet = self.item_info_window.cabinet_mech.text()
            amount = self.item_info_window.amount_mech.text()
            notes = self.item_info_window.notes_mech.text()
            database_mech.add_row(description, part_number,
                                  category, cabinet, amount, notes)

        self.load_data()

    def search(self):
        if self.key == "ELECTRONICS":
            description = self.item_info_window.description_ee.text()
            part_number = self.item_info_window.part_number_ee.text()
            category = self.item_info_window.category_ee.itemText(
                self.item_info_window.category_ee.currentIndex())
            package = self.item_info_window.package_ee.text()
            value = self.item_info_window.value_ee.text()
            unit = self.item_info_window.unit_ee.itemText(
                self.item_info_window.unit_ee.currentIndex())
            cabinet = self.item_info_window.cabinet_ee.text()
            amount = self.item_info_window.amount_ee.text()
            notes = self.item_info_window.notes_ee.text()

            self.result = database_ee.search_rows(
                description, part_number, category, package, value, unit, cabinet, amount, notes)

        elif self.key == "MECHANICS":
            description = self.item_info_window.description_mech.text()
            part_number = self.item_info_window.part_number_mech.text()
            category = self.item_info_window.category_mech.itemText(
                self.item_info_window.category_mech.currentIndex())
            cabinet = self.item_info_window.cabinet_mech.text()
            amount = self.item_info_window.amount_mech.text()
            notes = self.item_info_window.notes_mech.text()
            self.result = database_mech.search_rows(
                description, part_number, category, cabinet, amount, notes)

        self.display()

    def search_item(self, id):
        id = self.search_box.text()
        try:
            if self.key == "ELECTRONICS":
                first_matched_item = database_ee.search_row(id)
                self.item_info_window.item_ee_id_label.setText(
                    "Item id:{:>35}".format(id))
                self.item_info_window.description_ee.setText(
                    str(first_matched_item[1]))
                self.item_info_window.part_number_ee.setText(
                    str(first_matched_item[2]))
                self.item_info_window.category_ee.setCurrentText(
                    first_matched_item[3])
                self.item_info_window.package_ee.setText(
                    str(first_matched_item[4]))
                self.item_info_window.value_ee.setText(
                    str(first_matched_item[5]))
                self.item_info_window.unit_ee.setCurrentText(
                    first_matched_item[6])
                self.item_info_window.cabinet_ee.setText(
                    str(first_matched_item[7]))
                self.item_info_window.amount_ee .setText(
                    str(first_matched_item[8]))
                self.item_info_window.notes_ee.setText(
                    str(first_matched_item[9]))

            elif self.key == "MECHANICS":
                first_matched_item = database_mech.search_row(id)
                self.item_info_window.item_mech_id_label.setText(
                    "Item id:{:>35}".format(id))
                self.item_info_window.description_mech.setText(
                    str(first_matched_item[1]))
                self.item_info_window.part_number_mech.setText(
                    str(first_matched_item[2]))
                self.item_info_window.category_mech.setCurrentText(
                    first_matched_item[3])
                self.item_info_window.cabinet_mech.setText(
                    str(first_matched_item[4]))
                self.item_info_window.amount_mech .setText(
                    str(first_matched_item[5]))
                self.item_info_window.notes_mech.setText(
                    str(first_matched_item[6]))
        except Exception:
            if self.key == "ELECTRONICS":
                self.item_info_window.item_ee_id_label.setText("Item id:")
            elif self.key == "MECHANICS":
                self.item_info_window.item_mech_id_label.setText("Item id:")
            QMessageBox.information(
                QMessageBox(), "Search", "Can not find the item")

    def update(self):
        id = self.search_box.text()
        if self.key == "ELECTRONICS":
            description = self.item_info_window.description_ee.text()
            part_number = self.item_info_window.part_number_ee.text()
            category = self.item_info_window.category_ee.itemText(
                self.item_info_window.category_ee.currentIndex())
            package = self.item_info_window.package_ee.text()
            value = self.item_info_window.value_ee.text()
            unit = self.item_info_window.unit_ee.itemText(
                self.item_info_window.unit_ee.currentIndex())
            cabinet = self.item_info_window.cabinet_ee.text()
            amount = self.item_info_window.amount_ee.text()
            notes = self.item_info_window.notes_ee.text()
            database_ee.update_row(id, description, part_number, category,
                                   package, value, unit, cabinet, amount, notes)

        elif self.key == "MECHANICS":
            description = self.item_info_window.description_mech.text()
            part_number = self.item_info_window.part_number_mech.text()
            category = self.item_info_window.category_mech.itemText(
                self.item_info_window.category_mech.currentIndex())
            cabinet = self.item_info_window.cabinet_mech.text()
            amount = self.item_info_window.amount_mech.text()
            notes = self.item_info_window.notes_mech.text()
            database_mech.update_row(
                id, description, part_number, category, cabinet, amount, notes)

        QMessageBox.information(
            QMessageBox(), "Update", "Item has been updated.")
        self.load_data()

    def clear(self):
        if self.key == "ELECTRONICS":
            self.item_info_window.item_ee_id_label.setText("Item id:")
            self.item_info_window.description_ee.clear()
            self.item_info_window.part_number_ee.clear()
            self.item_info_window.package_ee.clear()
            self.item_info_window.value_ee.clear()
            self.item_info_window.cabinet_ee.clear()
            self.item_info_window.amount_ee.clear()
            self.item_info_window.notes_ee.clear()

        elif self.key == "MECHANICS":
            self.item_info_window.item_mech_id_label.setText("Item id:")
            self.item_info_window.description_mech.clear()
            self.item_info_window.part_number_mech.clear()
            self.item_info_window.cabinet_mech.clear()
            self.item_info_window.amount_mech.clear()
            self.item_info_window.notes_mech.clear()

    def clear_contents(self):
        self.tableWidget.clearContents()

    def delete(self):
        id = self.search_box.text()
        self.msgSearch = QMessageBox()
        try:
            if self.key == "ELECTRONICS":
                row = database_ee.search_row(id)
                search_result = "id:    "+str(row[0])+"\n"+"Description:     "+str(row[1])+"\n"+"Manufacturer Part No.:     "+str(row[2])+"\n"   \
                                + "Category:     "+str(row[3])+"\n"+"Package:     "+str(row[4])+"\n"+"Value:     "+str(row[5])+" " + str(row[6])+"\n" \
                                + "Cabinet:     " + \
                    str(row[7])+"\n"+"In stock amount:     " + \
                    str(row[8])+"\n"+"Notes:      "+str(row[9])
            elif self.key == "MECHANICS":
                row = database_mech.search_row(id)
                search_result = "id:    "+str(row[0])+"\n"+"Description:     "+str(row[1])+"\n"+"Manufacturer Part No.:     "+str(row[2])+"\n"   \
                                + "Category:     "+str(row[3])+"\n" + "Cabinet:     "+str(
                                    row[4])+"\n"+"In stock amount:     " + str(row[5])+"\n"+"Notes:      "+str(row[6])
            self.msgSearch.setText(search_result)
            self.msgSearch.setInformativeText(
                "Do you want to remove this item?")
            self.msgSearch.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.msgSearch.setWindowTitle("Remove item?")
            ret = self.msgSearch.exec_()
            if ret == QMessageBox.Yes:
                if self.key == "ELECTRONICS":
                    database_ee.delete_row(id)
                elif self.key == "MECHANICS":
                    database_mech.delete_row(id)
            elif ret == QMessageBox.No:
                pass
        except Exception:
            QMessageBox.warning(QMessageBox(), "Error",
                                "Could not remove the item")
        finally:
            self.load_data()

    # TODO: export different tables (electronic & mechanics) and set file path
    def export(self):
        try:
            if self.key == "ELECTRONICS":
                database_ee.to_csv()
            elif self.key == "MECHANICS":
                database_mech.to_csv()
            QMessageBox.information(
                QMessageBox(), "File export", "Export to CSV successfully")
        except Exception:
            QMessageBox.warning(QMessageBox(), "Error",
                                "Could not export to csv")
        finally:
            pass

    def quit(self):
        reply = QMessageBox.question(self, 'Exit', 'Do you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            sys.exit()
        else:
            pass


"""
A class that contains the software develop information
"""


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(500)
        self.setFixedHeight(250)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        self.setWindowTitle("About")
        title = QLabel("Laboratory Inventory System")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        labelpic = QLabel()
        pixmap = QPixmap('icon/logo.png')
        pixmap = pixmap.scaledToWidth(100)
        labelpic.setPixmap(pixmap)
        labelpic.setFixedHeight(100)

        layout.addWidget(title)
        layout.addWidget(QLabel("v1.0"))
        layout.addWidget(labelpic)
        layout.addWidget(QLabel("© Copyright Zhangshun Lu 2021"))

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


"""
Class of a window that displays the entry information
"""


class EntryWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        sub_layout = QVBoxLayout()
        self.setLayout(layout)

        # Label
        self.database_label = QLabel("Database")
        self.database_label.setFont(QFont("Arial", 14))
        self.database_label.setFixedSize(100, 30)
        self.item_label_ee = QLabel("Item Information")
        self.item_label_ee.setFont(QFont("Arial", 14))
        self.item_label_ee.setFixedSize(250, 40)
        self.item_label_mech = QLabel("Item Information")
        self.item_label_mech.setFont(QFont("Arial", 14))
        self.item_label_mech.setFixedSize(250, 40)

        self.picLabel = QLabel()
        self.pixmap = QPixmap("icon/electronics.jpg")
        self.pixmap = self.pixmap.scaled(300, 200, QtCore.Qt.KeepAspectRatio)
        self.picLabel.setPixmap(self.pixmap)
        self.picLabel.setFixedSize(300, 200)

        # Create and connect the combo box to switch between different inventory database
        self.pageCombo = QComboBox()
        self.pageCombo.addItems(
            ["ELECTRONICS", "MECHANICS", "QUALITY", "SOURCING"])
        self.pageCombo.activated.connect(self.switchPage)

        # Layouts
        self.stackedLayout = QStackedLayout()
        sub_layout.addWidget(self.database_label)
        sub_layout.addWidget(self.pageCombo)
        sub_layout.addWidget(self.picLabel)
        layout.addLayout(sub_layout)
        layout.addLayout(self.stackedLayout)

        # -------------------------- #
        #      Electronics Page      #
        # -------------------------- #
        self.page_ee = QWidget()
        self.page_ee_layout = QVBoxLayout()
        self.form_layout_ee = QFormLayout()

        self.item_ee_id = ""
        self.item_ee_id_label = QLabel("Item id:  " + self.item_ee_id)
        self.page_ee_layout.addWidget(self.item_label_ee)
        self.page_ee_layout.addWidget(self.item_ee_id_label)

        self.description_ee = QLineEdit()
        self.form_layout_ee.addRow("Description:", self.description_ee)

        self.part_number_ee = QLineEdit()
        self.form_layout_ee.addRow(
            "Manufacturer part number:", self.part_number_ee)

        self.category_ee = QComboBox()
        self.category_ee.addItem("Resistors", ["mΩ", "Ω", "kΩ", "MΩ"])
        self.category_ee.addItem("Capacitors", ["pF", "nF", "uF"])
        self.category_ee.addItem("Inductors", ["nH", "uH", "H"])
        self.category_ee.addItem("ICs", ["pcs"])
        self.category_ee.addItem("Modules", ["pcs"])
        self.category_ee.addItem("Motors", ["pcs"])
        self.category_ee.addItem("Batteries", ["pcs"])
        self.category_ee.addItem("Misc", ["pcs"])
        self.category_ee.currentIndexChanged.connect(self.updateUnitInput)
        self.form_layout_ee.addRow("Category:", self.category_ee)

        self.package_ee = QLineEdit()
        self.form_layout_ee.addRow("Package:", self.package_ee)

        self.value_ee = QLineEdit()
        self.form_layout_ee.addRow("Value:", self.value_ee)

        self.unit_ee = QComboBox()
        # default displays
        self.unit_ee.addItems(["mΩ", "Ω", "kΩ", "MΩ"])
        self.form_layout_ee.addRow("Unit:", self.unit_ee)

        self.cabinet_ee = QLineEdit()
        self.form_layout_ee.addRow("Cabinet:", self.cabinet_ee)

        self.amount_ee = QLineEdit()
        self.form_layout_ee.addRow("In stock amount:", self.amount_ee)

        self.notes_ee = QLineEdit()
        self.form_layout_ee.addRow("Notes:", self.notes_ee)

        self.page_ee_layout.addLayout(self.form_layout_ee)

        self.page_ee.setLayout(self.page_ee_layout)
        self.stackedLayout.addWidget(self.page_ee)

        # -------------------------- #
        #       Mechanics Page       #
        # -------------------------- #
        self.page_mech = QWidget()
        self.page_mech_layout = QVBoxLayout()
        self.form_layout_mech = QFormLayout()

        self.item_mech_id = ""
        self.item_mech_id_label = QLabel("Item id:  " + self.item_mech_id)
        self.page_mech_layout.addWidget(self.item_label_mech)
        self.page_mech_layout.addWidget(self.item_mech_id_label)

        self.description_mech = QLineEdit()
        self.form_layout_mech.addRow("Description:", self.description_mech)

        self.part_number_mech = QLineEdit()
        self.form_layout_mech.addRow(
            "Manufacturer part number:", self.part_number_mech)

        self.category_mech = QComboBox()
        self.category_mech.addItem("Screws and screw headers")
        self.category_mech.addItem("3D printing filament")
        self.category_mech.addItem("Tools")
        self.category_mech.addItem("Misc")
        self.form_layout_mech.addRow("Category:", self.category_mech)

        self.cabinet_mech = QLineEdit()
        self.form_layout_mech.addRow("Cabinet:", self.cabinet_mech)

        self.amount_mech = QLineEdit()
        self.form_layout_mech.addRow("In stock amount:", self.amount_mech)

        self.notes_mech = QLineEdit()
        self.form_layout_mech.addRow("Notes:", self.notes_mech)

        self.page_mech_layout.addLayout(self.form_layout_mech)

        for i in range(3):      # Add three empty boxes to better layout
            self.page_mech_layout.addWidget(QLabel())

        self.page_mech.setLayout(self.page_mech_layout)
        self.stackedLayout.addWidget(self.page_mech)

        # index of database
        # 0 = electronics, 1 = mechanics
        self.db_id = 0

    def updateUnitInput(self, index):
        self.unit_ee.clear()
        categories = self.category_ee.itemData(index)
        if categories:
            self.unit_ee.addItems(categories)

    def switchPage(self):
        self.stackedLayout.setCurrentIndex(self.pageCombo.currentIndex())
        self.db_id = self.pageCombo.currentIndex()
        return self.db_id


if __name__ == "__main__":
    database_exists = os.path.isfile("inventory.db")

    if database_exists:
        open("inventory.db", "r+")
    else:
        open("inventory.db", "w")
        database_ee.create_table_ee()
        database_mech.create_table_mech()

    app = QApplication(sys.argv)
    if QDialog.Accepted:
        window = MainWindow()
        window.show()
        window.key = "ELECTRONICS"      # select the electronics page as default
        window.load_data()
    sys.exit(app.exec_())

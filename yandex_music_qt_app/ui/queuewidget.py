# Form implementation generated from reading ui file '.\queuewidget.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets


class Ui_QueueWidget(object):
    def setupUi(self, QueueWidget):
        QueueWidget.setObjectName("QueueWidget")
        QueueWidget.resize(572, 495)
        QueueWidget.setMinimumSize(QtCore.QSize(572, 495))
        self.verticalLayout = QtWidgets.QVBoxLayout(QueueWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(parent=QueueWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(260)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(39)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.delete_element_from_queue = QtWidgets.QPushButton(parent=QueueWidget)
        self.delete_element_from_queue.setObjectName("delete_element_from_queue")
        self.horizontalLayout.addWidget(self.delete_element_from_queue)
        self.close_queue_window = QtWidgets.QPushButton(parent=QueueWidget)
        self.close_queue_window.setObjectName("close_queue_window")
        self.horizontalLayout.addWidget(self.close_queue_window)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(QueueWidget)
        QtCore.QMetaObject.connectSlotsByName(QueueWidget)

    def retranslateUi(self, QueueWidget):
        _translate = QtCore.QCoreApplication.translate
        QueueWidget.setWindowTitle(_translate("QueueWidget", "Очередь"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("QueueWidget", "Название"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("QueueWidget", "Исполнитель"))
        self.delete_element_from_queue.setText(_translate("QueueWidget", "Удалить"))
        self.close_queue_window.setText(_translate("QueueWidget", "Закрыть"))

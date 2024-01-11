# Form implementation generated from reading ui file '.\about.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(388, 269)
        Form.setMinimumSize(QtCore.QSize(388, 269))
        Form.setMaximumSize(QtCore.QSize(388, 269))
        Form.setStyleSheet(
            "background-color: rgb(81, 81, 81);\n" "color: rgb(255, 255, 255);"
        )
        self.pushButton = QtWidgets.QPushButton(parent=Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 81, 81))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icon/yandexlogo.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(100, 100))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(110, 10, 281, 81))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 291, 20))
        font = QtGui.QFont()
        font.setFamily("Fira Sans")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 121, 20))
        font = QtGui.QFont()
        font.setFamily("Fira Sans")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=Form)
        self.label_4.setGeometry(QtCore.QRect(10, 150, 121, 20))
        font = QtGui.QFont()
        font.setFamily("Fira Sans")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label_4.setOpenExternalLinks(True)
        self.label_4.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextBrowserInteraction
        )
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(parent=Form)
        self.label_5.setGeometry(QtCore.QRect(10, 170, 121, 46))
        font = QtGui.QFont()
        font.setFamily("Fira Sans")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_5.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label_5.setOpenExternalLinks(True)
        self.label_5.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextBrowserInteraction
        )
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "About"))
        self.label.setText(_translate("Form", "Yandex.Music Qt"))
        self.label_2.setText(_translate("Form", "By Alexander Borzov"))
        self.label_3.setText(_translate("Form", "Version: 0.1.0"))
        self.label_4.setText(
            _translate(
                "Form",
                '<html><head/><body><p>icons by <a href="https://icons8.com"><span style=" text-decoration: underline; color:#ffffff;">icons8.com</span></a></p></body></html>',
            )
        )
        self.label_5.setText(
            _translate(
                "Form",
                '<html><head/><body><p><a href="https://github.com/borzoff/yandex-music-qt-app"><span style=" text-decoration: underline; color:#ffffff;">GitHub</span></a></p><p><a href="https://borzoff.github.io/"><span style=" text-decoration: underline; color:#ffffff;">borzoff.github.io</span></a></p></body></html>',
            )
        )
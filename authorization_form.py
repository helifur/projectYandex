# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Login_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(346, 252)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.loginEdit = QtWidgets.QLineEdit(Form)
        self.loginEdit.setObjectName("loginEdit")
        self.verticalLayout.addWidget(self.loginEdit)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.passwordEdit = QtWidgets.QLineEdit(Form)
        self.passwordEdit.setObjectName("passwordEdit")
        self.verticalLayout.addWidget(self.passwordEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.loginButton = QtWidgets.QPushButton(Form)
        self.loginButton.setObjectName("loginButton")
        self.verticalLayout_2.addWidget(self.loginButton)
        self.registerButton = QtWidgets.QPushButton(Form)
        self.registerButton.setObjectName("registerButton")
        self.verticalLayout_2.addWidget(self.registerButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Войти"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Логин</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Пароль</span></p></body></html>"))
        self.loginButton.setText(_translate("Form", "Войти"))
        self.registerButton.setText(_translate("Form", "Зарегистрироваться"))
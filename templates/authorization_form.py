# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/authorization.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Authorize_Form(object):
    def setupUi(self, Authorize_Form):
        Authorize_Form.setObjectName("Authorize_Form")
        Authorize_Form.resize(283, 183)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui\\../auth_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Authorize_Form.setWindowIcon(icon)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Authorize_Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Authorize_Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.loginEdit = QtWidgets.QLineEdit(Authorize_Form)
        self.loginEdit.setObjectName("loginEdit")
        self.verticalLayout.addWidget(self.loginEdit)
        self.label_2 = QtWidgets.QLabel(Authorize_Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.passwordEdit = QtWidgets.QLineEdit(Authorize_Form)
        self.passwordEdit.setObjectName("passwordEdit")
        self.verticalLayout.addWidget(self.passwordEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.loginButton = QtWidgets.QPushButton(Authorize_Form)
        self.loginButton.setObjectName("loginButton")
        self.verticalLayout_2.addWidget(self.loginButton)

        self.retranslateUi(Authorize_Form)
        QtCore.QMetaObject.connectSlotsByName(Authorize_Form)

    def retranslateUi(self, Authorize_Form):
        _translate = QtCore.QCoreApplication.translate
        Authorize_Form.setWindowTitle(_translate("Authorize_Form", "Авторизация"))
        self.label.setText(_translate("Authorize_Form", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Логин</span></p></body></html>"))
        self.label_2.setText(_translate("Authorize_Form", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Пароль</span></p></body></html>"))
        self.loginButton.setText(_translate("Authorize_Form", "Войти"))
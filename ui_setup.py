# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setup.ui'
#
# Created: Fri Jul 18 17:32:18 2014
#      by: PyQt4 UI code generator 4.11
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Setup(object):
    def setupUi(self, Setup):
        Setup.setObjectName(_fromUtf8("Setup"))
        Setup.resize(353, 283)
        self.buttonBox = QtGui.QDialogButtonBox(Setup)
        self.buttonBox.setGeometry(QtCore.QRect(-50, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.layoutWidget = QtGui.QWidget(Setup)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 33, 182, 61))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.gridLayoutWidget = QtGui.QWidget(Setup)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 120, 311, 95))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalSlider = QtGui.QSlider(self.gridLayoutWidget)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(5000)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setPageStep(30)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.gridLayout_2.addWidget(self.horizontalSlider, 1, 1, 1, 1)
        self.horizontalSlider_2 = QtGui.QSlider(self.gridLayoutWidget)
        self.horizontalSlider_2.setMaximum(600)
        self.horizontalSlider_2.setSingleStep(1)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName(_fromUtf8("horizontalSlider_2"))
        self.gridLayout_2.addWidget(self.horizontalSlider_2, 3, 1, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 1, 2, 1, 1)
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 3, 2, 1, 1)

        self.retranslateUi(Setup)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Setup.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Setup.reject)
        #QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), Setup.startPosChanged)
        #QtCore.QObject.connect(self.lineEdit_2, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), Setup.stopPosChanged)
        QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.label_5.setNum)
        QtCore.QObject.connect(self.horizontalSlider_2, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.label_6.setNum)
        QtCore.QMetaObject.connectSlotsByName(Setup)

    def retranslateUi(self, Setup):
        Setup.setWindowTitle(_translate("Setup", "Dialog", None))
        self.label_3.setText(_translate("Setup", "Start", None))
        self.label_2.setText(_translate("Setup", "Stop", None))
        self.label.setText(_translate("Setup", "Exposure", None))
        self.label_4.setText(_translate("Setup", "Gain", None))
        self.label_5.setText(_translate("Setup", "TextLabel", None))
        self.label_6.setText(_translate("Setup", "TextLabel", None))


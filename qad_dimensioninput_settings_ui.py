# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qad_dimensioninput_settings.ui'
#
# Created: Mon May 14 11:26:27 2018
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

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

class Ui_DimInput_Settings_Dialog(object):
    def setupUi(self, DimInput_Settings_Dialog):
        DimInput_Settings_Dialog.setObjectName(_fromUtf8("DimInput_Settings_Dialog"))
        DimInput_Settings_Dialog.resize(363, 346)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DimInput_Settings_Dialog.sizePolicy().hasHeightForWidth())
        DimInput_Settings_Dialog.setSizePolicy(sizePolicy)
        DimInput_Settings_Dialog.setMinimumSize(QtCore.QSize(363, 346))
        DimInput_Settings_Dialog.setMaximumSize(QtCore.QSize(363, 346))
        self.layoutWidget = QtGui.QWidget(DimInput_Settings_Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(100, 310, 251, 25))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.okButton = QtGui.QPushButton(self.layoutWidget)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(self.layoutWidget)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.helpButton = QtGui.QPushButton(self.layoutWidget)
        self.helpButton.setObjectName(_fromUtf8("helpButton"))
        self.horizontalLayout.addWidget(self.helpButton)
        self.groupBox = QtGui.QGroupBox(DimInput_Settings_Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 341, 291))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 231, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.radioShow1Dim = QtGui.QRadioButton(self.groupBox)
        self.radioShow1Dim.setGeometry(QtCore.QRect(10, 50, 311, 17))
        self.radioShow1Dim.setObjectName(_fromUtf8("radioShow1Dim"))
        self.radioShow2Dim = QtGui.QRadioButton(self.groupBox)
        self.radioShow2Dim.setGeometry(QtCore.QRect(10, 80, 311, 17))
        self.radioShow2Dim.setObjectName(_fromUtf8("radioShow2Dim"))
        self.radioShowMoreDim = QtGui.QRadioButton(self.groupBox)
        self.radioShowMoreDim.setGeometry(QtCore.QRect(10, 110, 311, 17))
        self.radioShowMoreDim.setObjectName(_fromUtf8("radioShowMoreDim"))
        self.checkAbsoluteAngle = QtGui.QCheckBox(self.groupBox)
        self.checkAbsoluteAngle.setGeometry(QtCore.QRect(30, 200, 151, 17))
        self.checkAbsoluteAngle.setObjectName(_fromUtf8("checkAbsoluteAngle"))
        self.checkResultingDim = QtGui.QCheckBox(self.groupBox)
        self.checkResultingDim.setGeometry(QtCore.QRect(30, 140, 151, 17))
        self.checkResultingDim.setObjectName(_fromUtf8("checkResultingDim"))
        self.checkLengthChange = QtGui.QCheckBox(self.groupBox)
        self.checkLengthChange.setGeometry(QtCore.QRect(30, 170, 151, 17))
        self.checkLengthChange.setObjectName(_fromUtf8("checkLengthChange"))
        self.checkAngleChange = QtGui.QCheckBox(self.groupBox)
        self.checkAngleChange.setGeometry(QtCore.QRect(190, 140, 141, 17))
        self.checkAngleChange.setObjectName(_fromUtf8("checkAngleChange"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(50, 240, 281, 41))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 240, 31, 31))
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qad/icons/lamp_on.png")))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(DimInput_Settings_Dialog)
        QtCore.QObject.connect(self.radioShowMoreDim, QtCore.SIGNAL(_fromUtf8("clicked()")), DimInput_Settings_Dialog.radioShowMoreDimChecked)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), DimInput_Settings_Dialog.reject)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL(_fromUtf8("clicked()")), DimInput_Settings_Dialog.ButtonBOX_Accepted)
        QtCore.QObject.connect(self.helpButton, QtCore.SIGNAL(_fromUtf8("clicked()")), DimInput_Settings_Dialog.ButtonHELP_Pressed)
        QtCore.QObject.connect(self.radioShow2Dim, QtCore.SIGNAL(_fromUtf8("clicked()")), DimInput_Settings_Dialog.radioShow2DimChecked)
        QtCore.QObject.connect(self.radioShow1Dim, QtCore.SIGNAL(_fromUtf8("clicked()")), DimInput_Settings_Dialog.radioShow1DimChecked)
        QtCore.QMetaObject.connectSlotsByName(DimInput_Settings_Dialog)

    def retranslateUi(self, DimInput_Settings_Dialog):
        DimInput_Settings_Dialog.setWindowTitle(_translate("DimInput_Settings_Dialog", "QAD - Dimension Input Settings", None))
        self.okButton.setText(_translate("DimInput_Settings_Dialog", "OK", None))
        self.cancelButton.setText(_translate("DimInput_Settings_Dialog", "Cancel", None))
        self.helpButton.setText(_translate("DimInput_Settings_Dialog", "?", None))
        self.groupBox.setTitle(_translate("DimInput_Settings_Dialog", "Visibility", None))
        self.label.setText(_translate("DimInput_Settings_Dialog", "When grip-stretching:", None))
        self.radioShow1Dim.setToolTip(_translate("DimInput_Settings_Dialog", "Displays only the length change dimensional input tooltip when you are using grip editing to stretch an object. (DYNDIVIS system variable)", None))
        self.radioShow1Dim.setText(_translate("DimInput_Settings_Dialog", "Show only 1 dimension input field at a time", None))
        self.radioShow2Dim.setToolTip(_translate("DimInput_Settings_Dialog", "Displays the length change and resulting dimensional input tooltips when you are using grip editing to stretch an object. (DYNDIVIS system variable)", None))
        self.radioShow2Dim.setText(_translate("DimInput_Settings_Dialog", "Show 2 dimension input fields at a time", None))
        self.radioShowMoreDim.setToolTip(_translate("DimInput_Settings_Dialog", "When you are using grip editing to stretch an object, displays the dimensional input tooltips that are selected below. (DYNDIVIS and DYNDIGRIP system variables)", None))
        self.radioShowMoreDim.setText(_translate("DimInput_Settings_Dialog", "Show the following dimension input fields simultaneously:", None))
        self.checkAbsoluteAngle.setToolTip(_translate("DimInput_Settings_Dialog", "Displays an angle dimensional tooltip that is updated as you move the grip.", None))
        self.checkAbsoluteAngle.setText(_translate("DimInput_Settings_Dialog", "Absolute angle", None))
        self.checkResultingDim.setToolTip(_translate("DimInput_Settings_Dialog", "Displays a length dimensional tooltip that is updated as you move the grip.", None))
        self.checkResultingDim.setText(_translate("DimInput_Settings_Dialog", "Resulting dimension", None))
        self.checkLengthChange.setToolTip(_translate("DimInput_Settings_Dialog", "Displays the change in length as you move the grip.", None))
        self.checkLengthChange.setText(_translate("DimInput_Settings_Dialog", "Length change", None))
        self.checkAngleChange.setToolTip(_translate("DimInput_Settings_Dialog", "Displays the change in the angle as you move the grip.", None))
        self.checkAngleChange.setText(_translate("DimInput_Settings_Dialog", "Angle change", None))
        self.label_2.setText(_translate("DimInput_Settings_Dialog", "Press TAB to switch to the next dimension input field", None))


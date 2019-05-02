# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qad_pointerinput_settings.ui'
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

class Ui_PointerInput_Settings_Dialog(object):
    def setupUi(self, PointerInput_Settings_Dialog):
        PointerInput_Settings_Dialog.setObjectName(_fromUtf8("PointerInput_Settings_Dialog"))
        PointerInput_Settings_Dialog.resize(272, 356)
        PointerInput_Settings_Dialog.setMinimumSize(QtCore.QSize(272, 356))
        PointerInput_Settings_Dialog.setMaximumSize(QtCore.QSize(272, 356))
        self.groupBox = QtGui.QGroupBox(PointerInput_Settings_Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 251, 181))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 231, 41))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 60, 231, 51))
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.radioPolarFmt = QtGui.QRadioButton(self.groupBox_3)
        self.radioPolarFmt.setGeometry(QtCore.QRect(10, 10, 211, 17))
        self.radioPolarFmt.setObjectName(_fromUtf8("radioPolarFmt"))
        self.radioCartesianFmt = QtGui.QRadioButton(self.groupBox_3)
        self.radioCartesianFmt.setGeometry(QtCore.QRect(10, 30, 211, 17))
        self.radioCartesianFmt.setObjectName(_fromUtf8("radioCartesianFmt"))
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 120, 231, 51))
        self.groupBox_4.setTitle(_fromUtf8(""))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.radioRelativeCoord = QtGui.QRadioButton(self.groupBox_4)
        self.radioRelativeCoord.setGeometry(QtCore.QRect(10, 10, 211, 17))
        self.radioRelativeCoord.setObjectName(_fromUtf8("radioRelativeCoord"))
        self.radioAbsoluteCoord = QtGui.QRadioButton(self.groupBox_4)
        self.radioAbsoluteCoord.setGeometry(QtCore.QRect(10, 30, 211, 17))
        self.radioAbsoluteCoord.setObjectName(_fromUtf8("radioAbsoluteCoord"))
        self.groupBox_2 = QtGui.QGroupBox(PointerInput_Settings_Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 210, 251, 101))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.radioVisAlways = QtGui.QRadioButton(self.groupBox_2)
        self.radioVisAlways.setGeometry(QtCore.QRect(10, 80, 231, 17))
        self.radioVisAlways.setObjectName(_fromUtf8("radioVisAlways"))
        self.radioVisWhenAsksPt = QtGui.QRadioButton(self.groupBox_2)
        self.radioVisWhenAsksPt.setGeometry(QtCore.QRect(10, 60, 231, 17))
        self.radioVisWhenAsksPt.setObjectName(_fromUtf8("radioVisWhenAsksPt"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 231, 31))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.layoutWidget = QtGui.QWidget(PointerInput_Settings_Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 320, 251, 25))
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

        self.retranslateUi(PointerInput_Settings_Dialog)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PointerInput_Settings_Dialog.ButtonBOX_Accepted)
        QtCore.QObject.connect(self.helpButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PointerInput_Settings_Dialog.ButtonHELP_Pressed)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PointerInput_Settings_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PointerInput_Settings_Dialog)

    def retranslateUi(self, PointerInput_Settings_Dialog):
        PointerInput_Settings_Dialog.setWindowTitle(_translate("PointerInput_Settings_Dialog", "QAD - Pointer Input Settings", None))
        self.groupBox.setTitle(_translate("PointerInput_Settings_Dialog", "Format", None))
        self.label.setText(_translate("PointerInput_Settings_Dialog", "For second or next points, default to:", None))
        self.radioPolarFmt.setToolTip(_translate("PointerInput_Settings_Dialog", "Displays the tooltip for the second or next point in polar coordinate format. Enter a comma (,) to change to Cartesian format. (DYNPIFORMAT system variable)", None))
        self.radioPolarFmt.setText(_translate("PointerInput_Settings_Dialog", "Polar format", None))
        self.radioCartesianFmt.setToolTip(_translate("PointerInput_Settings_Dialog", "Displays the tooltip for the second or next point in Cartesian coordinate format. Enter an angle symbol (<) to change to polar format. (DYNPIFORMAT system variable)", None))
        self.radioCartesianFmt.setText(_translate("PointerInput_Settings_Dialog", "Cartesian format", None))
        self.radioRelativeCoord.setToolTip(_translate("PointerInput_Settings_Dialog", "Displays the tooltip for the second or next point in relative coordinate format. Enter a pound sign (#) to change to absolute format. (DYNPICOORDS system variable)", None))
        self.radioRelativeCoord.setText(_translate("PointerInput_Settings_Dialog", "Relative coordinates", None))
        self.radioAbsoluteCoord.setToolTip(_translate("PointerInput_Settings_Dialog", "Displays the tooltip for the second or next point in absolute coordinate format. Enter an \"at\" sign (@) to change to relative coordinates format. (DYNPICOORDS system variable)", None))
        self.radioAbsoluteCoord.setText(_translate("PointerInput_Settings_Dialog", "Absolute coordinates", None))
        self.groupBox_2.setTitle(_translate("PointerInput_Settings_Dialog", "Visibility", None))
        self.radioVisAlways.setToolTip(_translate("PointerInput_Settings_Dialog", "Always displays tooltips when pointer input is turned on. ( DYNPIVIS system variable)", None))
        self.radioVisAlways.setText(_translate("PointerInput_Settings_Dialog", "Always - even when not in command", None))
        self.radioVisWhenAsksPt.setToolTip(_translate("PointerInput_Settings_Dialog", "When pointer input is turned on, displays tooltips whenever a command prompts you for a point. (DYNPIVIS system variable)", None))
        self.radioVisWhenAsksPt.setText(_translate("PointerInput_Settings_Dialog", "When a command asks for a point", None))
        self.label_2.setText(_translate("PointerInput_Settings_Dialog", "Show coordinate tooltips:", None))
        self.okButton.setText(_translate("PointerInput_Settings_Dialog", "OK", None))
        self.cancelButton.setText(_translate("PointerInput_Settings_Dialog", "Cancel", None))
        self.helpButton.setText(_translate("PointerInput_Settings_Dialog", "?", None))


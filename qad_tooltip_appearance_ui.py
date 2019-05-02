# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qad_tooltip_appearance.ui'
#
# Created: Mon May 14 11:26:29 2018
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

class Ui_ToolTipAppearance_Dialog(object):
    def setupUi(self, ToolTipAppearance_Dialog):
        ToolTipAppearance_Dialog.setObjectName(_fromUtf8("ToolTipAppearance_Dialog"))
        ToolTipAppearance_Dialog.resize(379, 366)
        ToolTipAppearance_Dialog.setMinimumSize(QtCore.QSize(379, 366))
        ToolTipAppearance_Dialog.setMaximumSize(QtCore.QSize(379, 366))
        self.widget_Preview = QtGui.QWidget(ToolTipAppearance_Dialog)
        self.widget_Preview.setGeometry(QtCore.QRect(20, 20, 191, 71))
        self.widget_Preview.setObjectName(_fromUtf8("widget_Preview"))
        self.Button_TooltipColors = QtGui.QPushButton(ToolTipAppearance_Dialog)
        self.Button_TooltipColors.setGeometry(QtCore.QRect(20, 100, 75, 23))
        self.Button_TooltipColors.setObjectName(_fromUtf8("Button_TooltipColors"))
        self.groupBox = QtGui.QGroupBox(ToolTipAppearance_Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 130, 351, 51))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(10, 20, 113, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 0, 351, 51))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.edit_size = QtGui.QLineEdit(self.groupBox_2)
        self.edit_size.setGeometry(QtCore.QRect(10, 20, 113, 20))
        self.edit_size.setObjectName(_fromUtf8("edit_size"))
        self.slider_size = QtGui.QSlider(self.groupBox_2)
        self.slider_size.setGeometry(QtCore.QRect(130, 20, 211, 22))
        self.slider_size.setPageStep(1)
        self.slider_size.setOrientation(QtCore.Qt.Horizontal)
        self.slider_size.setObjectName(_fromUtf8("slider_size"))
        self.groupBox_3 = QtGui.QGroupBox(ToolTipAppearance_Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 190, 351, 51))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.slider_transparency = QtGui.QSlider(self.groupBox_3)
        self.slider_transparency.setGeometry(QtCore.QRect(130, 20, 211, 22))
        self.slider_transparency.setOrientation(QtCore.Qt.Horizontal)
        self.slider_transparency.setObjectName(_fromUtf8("slider_transparency"))
        self.edit_transparency = QtGui.QLineEdit(self.groupBox_3)
        self.edit_transparency.setGeometry(QtCore.QRect(10, 20, 113, 20))
        self.edit_transparency.setObjectName(_fromUtf8("edit_transparency"))
        self.horizontalLayoutWidget = QtGui.QWidget(ToolTipAppearance_Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(120, 330, 251, 25))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.Button_OK = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.Button_OK.setObjectName(_fromUtf8("Button_OK"))
        self.horizontalLayout.addWidget(self.Button_OK)
        self.Button_Cancel = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.Button_Cancel.setObjectName(_fromUtf8("Button_Cancel"))
        self.horizontalLayout.addWidget(self.Button_Cancel)
        self.Button_Help = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.Button_Help.setObjectName(_fromUtf8("Button_Help"))
        self.horizontalLayout.addWidget(self.Button_Help)
        self.groupBox_4 = QtGui.QGroupBox(ToolTipAppearance_Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 250, 351, 71))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.radio_for_all_tooltips = QtGui.QRadioButton(self.groupBox_4)
        self.radio_for_all_tooltips.setGeometry(QtCore.QRect(20, 20, 321, 17))
        self.radio_for_all_tooltips.setObjectName(_fromUtf8("radio_for_all_tooltips"))
        self.radio_for_DI_tooltips = QtGui.QRadioButton(self.groupBox_4)
        self.radio_for_DI_tooltips.setGeometry(QtCore.QRect(20, 40, 321, 17))
        self.radio_for_DI_tooltips.setObjectName(_fromUtf8("radio_for_DI_tooltips"))

        self.retranslateUi(ToolTipAppearance_Dialog)
        QtCore.QObject.connect(self.Button_TooltipColors, QtCore.SIGNAL(_fromUtf8("clicked()")), ToolTipAppearance_Dialog.Button_TooltipColors_Pressed)
        QtCore.QObject.connect(self.Button_Cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), ToolTipAppearance_Dialog.reject)
        QtCore.QObject.connect(self.slider_size, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), ToolTipAppearance_Dialog.slider_size_moved)
        QtCore.QObject.connect(self.edit_size, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), ToolTipAppearance_Dialog.edit_size_textChanged)
        QtCore.QObject.connect(self.edit_transparency, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), ToolTipAppearance_Dialog.edit_transparency_textChanged)
        QtCore.QObject.connect(self.slider_transparency, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), ToolTipAppearance_Dialog.slider_transparency_moved)
        QtCore.QObject.connect(self.Button_OK, QtCore.SIGNAL(_fromUtf8("clicked()")), ToolTipAppearance_Dialog.ButtonBOX_Accepted)
        QtCore.QObject.connect(self.Button_Help, QtCore.SIGNAL(_fromUtf8("clicked()")), ToolTipAppearance_Dialog.ButtonHELP_Pressed)
        QtCore.QMetaObject.connectSlotsByName(ToolTipAppearance_Dialog)

    def retranslateUi(self, ToolTipAppearance_Dialog):
        ToolTipAppearance_Dialog.setWindowTitle(_translate("ToolTipAppearance_Dialog", "QAD - Tooltip appearance", None))
        self.Button_TooltipColors.setToolTip(_translate("ToolTipAppearance_Dialog", "Displays the Drawing Window Colors dialog box, where you can specify a color for drafting tooltips and their backgrounds in a specified context.", None))
        self.Button_TooltipColors.setText(_translate("ToolTipAppearance_Dialog", "Colors...", None))
        self.groupBox.setTitle(_translate("ToolTipAppearance_Dialog", "Size", None))
        self.groupBox_2.setTitle(_translate("ToolTipAppearance_Dialog", "Size", None))
        self.edit_size.setToolTip(_translate("ToolTipAppearance_Dialog", "Specifies a size for tooltips. The default size is 0. Use the slider to make tooltips larger or smaller.", None))
        self.slider_size.setToolTip(_translate("ToolTipAppearance_Dialog", "Specifies a size for tooltips. The default size is 0. Use the slider to make tooltips larger or smaller.", None))
        self.groupBox_3.setTitle(_translate("ToolTipAppearance_Dialog", "Transparency", None))
        self.slider_transparency.setToolTip(_translate("ToolTipAppearance_Dialog", "Controls the transparency of tooltips. The lower the setting, the less transparent the tooltip. A value of 0 sets the tooltip to opaque.", None))
        self.edit_transparency.setToolTip(_translate("ToolTipAppearance_Dialog", "Controls the transparency of tooltips. The lower the setting, the less transparent the tooltip. A value of 0 sets the tooltip to opaque.", None))
        self.Button_OK.setText(_translate("ToolTipAppearance_Dialog", "OK", None))
        self.Button_Cancel.setText(_translate("ToolTipAppearance_Dialog", "Cancel", None))
        self.Button_Help.setText(_translate("ToolTipAppearance_Dialog", "?", None))
        self.groupBox_4.setTitle(_translate("ToolTipAppearance_Dialog", "Apply to:", None))
        self.radio_for_all_tooltips.setText(_translate("ToolTipAppearance_Dialog", "Override OS settings for all drafting tooltips", None))
        self.radio_for_DI_tooltips.setText(_translate("ToolTipAppearance_Dialog", "Use settings only for Dynamic Input tooltips", None))


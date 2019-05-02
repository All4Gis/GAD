# --------------------------------------------------------
#   GAD - Geographic Aided Design
#
#    begin      : May 05, 2019
#    copyright  : (c) 2019 by German Perez-Casanova Gomez
#    email      : icearqu@gmail.com
#
# --------------------------------------------------------
#   GAD  This program is free software and is distributed in
#   the hope that it will be useful, but without any warranty,
#   you can redistribute it and/or modify it under the terms
#   of version 3 of the GNU General Public License (GPL v3) as
#   published by the Free Software Foundation (www.gnu.org)
# --------------------------------------------------------



from PyQt5 import QtCore, QtGui, QtWidgets


from .qad_msg import QadMsg


class Ui_QadTextWindow(object):
    def setupUi(self, QadTextWindow):
        QadTextWindow.setObjectName("QadTextWindow")
        QadTextWindow.setWindowModality(QtCore.Qt.NonModal)
        QadTextWindow.setEnabled(True)
        QadTextWindow.resize(642, 193)
        QadTextWindow.setMinimumSize(100, 20)
        QadTextWindow.setMaximumSize(QtCore.QSize(524287, 524287))
                
        self.retranslateUi(QadTextWindow)
        QtCore.QMetaObject.connectSlotsByName(QadTextWindow)

    def retranslateUi(self, QadTextWindow):
       QadTextWindow.setWindowTitle(QadMsg.translate("Text_window", "QAD text window"))

class Ui_QadCmdSuggestWindow(object):
    def setupUi(self, QadCmdSuggestWindow):
        QadCmdSuggestWindow.setObjectName("QadCmdsListWindow")
        QadCmdSuggestWindow.setWindowModality(QtCore.Qt.NonModal)
        QadCmdSuggestWindow.setEnabled(True)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("QadCmdsListWindowDockWidgetContents")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.vboxlayout.setObjectName("QadCmdsListWindowVBoxLayout")
        self.vboxlayout.setMargin(0)
        QadCmdSuggestWindow.setLayout(self.vboxlayout)        
        QtCore.QMetaObject.connectSlotsByName(QadCmdSuggestWindow)



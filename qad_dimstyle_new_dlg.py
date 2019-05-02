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



# Import the PyQt and QGIS libraries
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog
from qgis.core import *
from qgis.core import QgsApplication
from qgis.utils import *

from .import qad_dimstyle_new_ui
from .qad_dimstyle_details_dlg import QadDIMSTYLE_DETAILS_Dialog

from .qad_variables import *
from .qad_dim import *
from .qad_msg import QadMsg, qadShowPluginHelp
from . import qad_utils


#######################################################################################
# Classe che gestisce l'interfaccia grafica della funzione di creazione nuovo stile
class QadDIMSTYLE_NEW_Dialog(QDialog, QObject, qad_dimstyle_new_ui.Ui_DimStyle_New_Dialog):
   def __init__(self, plugIn, parent, fromDimStyleName = None):
      self.plugIn = plugIn
      self.iface = self.plugIn.iface.mainWindow()

      QDialog.__init__(self, parent)
      
      self.newDimStyle = QadDimStyle()
      self.newDimStyleNameChanged = False
      
      self.setupUi(self)
                 
      self.dimNameList = []
      for dimStyle in QadDimStyles.dimStyleList: # lista degli stili di quotatura caricati
         self.DimStyleNameFrom.addItem(dimStyle.name, dimStyle)
         self.dimNameList.append(dimStyle.name)
      
      # sort
      self.DimStyleNameFrom.model().sort(0)

      # seleziono un elemento della lista
      if fromDimStyleName is not None:
         index = self.DimStyleNameFrom.findText(fromDimStyleName)
         self.DimStyleNameFrom.setCurrentIndex(index)
         self.DimStyleNameFromChanged(index)
      
   def DimStyleNameFromChanged(self, index):
      # leggo l'elemento selezionato
      dimStyle = self.DimStyleNameFrom.itemData(index)
      if dimStyle is not None:
         self.newDimStyle.set(dimStyle)
         if self.newDimStyleNameChanged == False:
            newName = qad_utils.checkUniqueNewName(dimStyle.name, self.dimNameList, QadMsg.translate("QAD", "Copy of "))
            if newName is not None:
               self.newDimStyleName.setText(newName)

   def newStyleNameChanged(self, text):
      self.newDimStyleNameChanged = True
         
   def ButtonBOX_continue(self):
      if self.newDimStyleName.text() in self.dimNameList:
         QMessageBox.critical(self, QadMsg.translate("QAD", "QAD"), \
                              QadMsg.translate("DimStyle_Dialog", "Dimension style name already existing. Specify a different name."))
         return False
      self.newDimStyle.name = self.newDimStyleName.text()
      self.newDimStyle.description = self.newDimStyleDescr.text()
      Form = QadDIMSTYLE_DETAILS_Dialog(self.plugIn, self, self.newDimStyle)
      title = QadMsg.translate("DimStyle_Dialog", "New dimension style: ") + self.newDimStyle.name
      Form.setWindowTitle(title)
      
      if Form.exec_() == QDialog.Accepted:
         self.dimStyle = Form.dimStyle
         QDialog.accept(self)
      else:
         self.dimStyle = None
         QDialog.reject(self)      

   def ButtonHELP_Pressed(self):
      qadShowPluginHelp(QadMsg.translate("Help", "Dimensioning"))

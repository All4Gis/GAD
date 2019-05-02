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
from qgis.core import *
from qgis.core import QgsApplication


from .qad_options_dlg import QadOPTIONSDialog


from .qad_generic_cmd import QadCommandClass
from .qad_msg import QadMsg


# Classe che gestisce il comando OPTIONS
class QadOPTIONSCommandClass(QadCommandClass):
   
   def instantiateNewCmd(self):
      """ istanzia un nuovo comando dello stesso tipo """
      return QadOPTIONSCommandClass(self.plugIn)
   
   def getName(self):
      return QadMsg.translate("Command_list", "OPTIONS")

   def getEnglishName(self):
      return "OPTIONS"

   def connectQAction(self, action):
      action.triggered.connect(self.plugIn.runOPTIONSCommand)

   def getIcon(self):
      return QIcon(":/plugins/qad/icons/options.svg")

   def getNote(self):
      # impostare le note esplicative del comando
      return QadMsg.translate("Command_OPTIONS", "QAD Options.")
   
   def __init__(self, plugIn):
      QadCommandClass.__init__(self, plugIn)
            
   def run(self, msgMapTool = False, msg = None):
      Form = QadOPTIONSDialog(self.plugIn)
      Form.exec_()
      return True
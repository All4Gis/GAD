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


from .qad_generic_cmd import QadCommandClass
from .qad_msg import QadMsg, qadShowPluginHelp


# Classe che gestisce il comando HELP
class QadHELPCommandClass(QadCommandClass):

   def instantiateNewCmd(self):
      """ istanzia un nuovo comando dello stesso tipo """
      return QadHELPCommandClass(self.plugIn)

   def getName(self):
      return QadMsg.translate("Command_list", "HELP")

   def getEnglishName(self):
      return "HELP"

   def connectQAction(self, action):
      action.triggered.connect(self.plugIn.runHELPCommand)

   def getIcon(self):
      return QIcon(":/plugins/qad/icons/help.svg")

   def getNote(self):
      # impostare le note esplicative del comando
      return QadMsg.translate("Command_HELP", "The QAD manual will be showed.")
   
   def __init__(self, plugIn):
      QadCommandClass.__init__(self, plugIn)
        
   def run(self, msgMapTool = False, msg = None):
      qadShowPluginHelp()       
      return True

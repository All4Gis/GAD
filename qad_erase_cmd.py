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
from .qad_msg import QadMsg
from .qad_getpoint import *
from .qad_ssget_cmd import QadSSGetClass
from . import qad_layer


# Classe che gestisce il comando ERASE
class QadERASECommandClass(QadCommandClass):

   def instantiateNewCmd(self):
      """ istanzia un nuovo comando dello stesso tipo """
      return QadERASECommandClass(self.plugIn)
   
   def getName(self):
      return QadMsg.translate("Command_list", "ERASE")

   def getEnglishName(self):
      return "ERASE"

   def connectQAction(self, action):
      action.triggered.connect(self.plugIn.runERASECommand)

   def getIcon(self):
      return QIcon(":/plugins/qad/icons/erase.png")

   def getNote(self):
      # impostare le note esplicative del comando
      return QadMsg.translate("Command_ERASE", "Removes objects of the map.")
   
   def __init__(self, plugIn):
      QadCommandClass.__init__(self, plugIn)
      self.SSGetClass = QadSSGetClass(plugIn)
      self.SSGetClass.onlyEditableLayers = True

   def __del__(self):
      QadCommandClass.__del__(self)
      del self.SSGetClass
      
   def getPointMapTool(self, drawMode = QadGetPointDrawModeEnum.NONE):
      if self.step == 0: # quando si é in fase di selezione entità
         return self.SSGetClass.getPointMapTool(drawMode)
      else:
         return QadCommandClass.getPointMapTool(self, drawMode)

   def run(self, msgMapTool = False, msg = None):
            
      #=========================================================================
      # RICHIESTA PRIMO PUNTO PER SELEZIONE OGGETTI
      if self.step == 0: # inizio del comando
         if self.SSGetClass.run(msgMapTool, msg) == True:
            # selezione terminata
            self.step = 1
            return self.run(msgMapTool, msg)
         else:
            return False
      
      #=========================================================================
      # CANCELLAZIONE OGGETTI
      elif self.step == 1:
         self.plugIn.beginEditCommand("Feature deleted", self.SSGetClass.entitySet.getLayerList())
              
         for layerEntitySet in self.SSGetClass.entitySet.layerEntitySetList:
            # plugIn, layer, featureIds, refresh
            if qad_layer.deleteFeaturesToLayer(self.plugIn, layerEntitySet.layer, \
                                               layerEntitySet.featureIds, False) == False:
               self.plugIn.destroyEditCommand()
               return
            
         self.plugIn.endEditCommand()
            
         return True # fine comando


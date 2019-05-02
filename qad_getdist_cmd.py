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
from .qad_textwindow import *
from .qad_getpoint import *
from . import qad_utils


#===============================================================================
# QadGetDistClass
#===============================================================================
class QadGetDistClass(QadCommandClass):

   def instantiateNewCmd(self):
      """ istanzia un nuovo comando dello stesso tipo """
      return QadGetDistClass(self.plugIn)
      
   def __init__(self, plugIn):
      QadCommandClass.__init__(self, plugIn)
      self.entity = QadEntity()
      self.startPt = None            
      self.msg = QadMsg.translate("QAD", "Specify the distance: ")
      self.dist = None
      self.inputMode = QadInputModeEnum.NOT_ZERO | QadInputModeEnum.NOT_NEGATIVE
      self.ctrlKey = False

      # memorizzo last point perchè il/i punto/i indicato/i da questa questa funzione non devono
      # alterare lastpoint 
      self.__prevLastPoint = self.plugIn.lastPoint
            
   def run(self, msgMapTool = False, msg = None):
      if self.plugIn.canvas.mapSettings().destinationCrs().isGeographic():
         self.showMsg(QadMsg.translate("QAD", "\nThe coordinate reference system of the project must be a projected coordinate system.\n"))
         return True # fine comando

      #=========================================================================
      # RICHIESTA PUNTO o ENTITA'
      if self.step == 0: # inizio del comando
         # si appresta ad attendere un punto o un numero reale         
         # msg, inputType, default, keyWords, valori positivi
         self.waitFor(self.msg, \
                      QadInputTypeEnum.POINT2D | QadInputTypeEnum.FLOAT, \
                      self.dist, "", \
                      QadInputModeEnum.NOT_NULL | self.inputMode)
         
         if self.startPt is not None:            
            # imposto il map tool
            self.getPointMapTool().setDrawMode(QadGetPointDrawModeEnum.ELASTIC_LINE)
            self.getPointMapTool().setStartPoint(self.startPt)

         self.step = 1
         return False

      #=========================================================================
      # RISPOSTA ALLA RICHIESTA PUNTO o numero reale
      elif self.step == 1: # dopo aver atteso un punto si riavvia il comando
         if msgMapTool == True: # il punto arriva da una selezione grafica
            # la condizione seguente si verifica se durante la selezione di un punto
            # é stato attivato un altro plugin che ha disattivato Qad
            # quindi stato riattivato il comando che torna qui senza che il maptool
            # abbia selezionato un punto            
            if self.getPointMapTool().point is None: # il maptool é stato attivato senza un punto
               if self.getPointMapTool().rightButton == True: # se usato il tasto destro del mouse
                  return True # fine comando
               else:
                  self.setMapTool(self.getPointMapTool()) # riattivo il maptool
                  return False
               
            value = self.getPointMapTool().point
            self.ctrlKey = self.getPointMapTool().ctrlKey
         else: # il punto o il numero reale arriva come parametro della funzione
            value = msg

         if value is None:
            return True # fine comando
         
         if type(value) == float:
            self.dist = value
            return True # fine comando
         elif type(value) == QgsPointXY:
            # il/i punto/i indicato/i da questa questa funzione non devono alterare lastpoint 
            self.plugIn.setLastPoint(self.__prevLastPoint)

            if self.startPt is not None:
               self.dist = qad_utils.getDistance(self.startPt, value)
               return True # fine comando
            else:
               self.startPt = value            
               # imposto il map tool
               self.getPointMapTool().setDrawMode(QadGetPointDrawModeEnum.ELASTIC_LINE)
               self.getPointMapTool().setStartPoint(self.startPt)
               
               # si appresta ad attendere un punto
               self.waitForPoint(QadMsg.translate("QAD", "Specify second point: "))
                              
               self.step = 2

         return False
         
      #=========================================================================
      # RISPOSTA ALLA RICHIESTA SECONDO PUNTO DELLA DISTANZA (da step = 1)
      elif self.step == 2: # dopo aver atteso un punto si riavvia il comando
         if msgMapTool == True: # il punto arriva da una selezione grafica
            # la condizione seguente si verifica se durante la selezione di un punto
            # é stato attivato un altro plugin che ha disattivato Qad
            # quindi stato riattivato il comando che torna qui senza che il maptool
            # abbia selezionato un punto            
            if self.getPointMapTool().point is None: # il maptool é stato attivato senza un punto
               if self.getPointMapTool().rightButton == True: # se usato il tasto destro del mouse
                  return True # fine comando
               else:
                  self.setMapTool(self.getPointMapTool()) # riattivo il maptool
                  return False

            value = self.getPointMapTool().point
         else: # il punto arriva come parametro della funzione
            value = msg

         # il/i punto/i indicato/i da questa questa funzione non devono alterare lastpoint 
         self.plugIn.setLastPoint(self.__prevLastPoint)

         self.dist = qad_utils.getDistance(self.startPt, value)
         return True # fine comando
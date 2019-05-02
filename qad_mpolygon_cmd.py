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
from .qad_pline_cmd import QadPLINECommandClass
from .qad_msg import QadMsg
from .qad_textwindow import *
from .qad_getpoint import *
from . import qad_utils
from . import qad_layer


# Classe che gestisce il comando MPOLYGON
class QadMPOLYGONCommandClass(QadCommandClass):

   def instantiateNewCmd(self):
      """ istanzia un nuovo comando dello stesso tipo """
      return QadMPOLYGONCommandClass(self.plugIn)
   
   def getName(self):
      return QadMsg.translate("Command_list", "MPOLYGON")

   def getEnglishName(self):
      return "MPOLYGON"

   def connectQAction(self, action):
      action.triggered.connect(self.plugIn.runMPOLYGONCommand)

   def getIcon(self):
      return QIcon(":/plugins/qad/icons/mpolygon.svg")

   def getNote(self):
      # impostare le note esplicative del comando      
      return QadMsg.translate("Command_MPOLYGON", "Draws a polygon by many methods.\nA Polygon is a closed sequence of straight line segments,\narcs or a combination of two.")
   
   def __init__(self, plugIn):
      QadCommandClass.__init__(self, plugIn)
      self.vertices = []
      # se questo flag = True il comando serve all'interno di un altro comando per disegnare un poligono
      # che non verrà salvato su un layer
      self.virtualCmd = False
      self.rubberBandBorderColor = None
      self.rubberBandFillColor = None
      self.PLINECommand = None

   def __del__(self):
      QadCommandClass.__del__(self)
      if self.PLINECommand is not None:
         del self.PLINECommand


   def getPointMapTool(self, drawMode = QadGetPointDrawModeEnum.NONE):
      if self.PLINECommand is not None:
         return self.PLINECommand.getPointMapTool(drawMode)
      else:
         return QadCommandClass.getPointMapTool(self, drawMode)


   def getCurrentContextualMenu(self):
      if self.PLINECommand is not None:
         return self.PLINECommand.getCurrentContextualMenu()
      else:
         return self.contextualMenu


   def setRubberBandColor(self, rubberBandBorderColor, rubberBandFillColor):
      self.rubberBandBorderColor = rubberBandBorderColor
      self.rubberBandFillColor = rubberBandFillColor
      if self.PLINECommand is not None:
         self.PLINECommand.setRubberBandColor(rubberBandBorderColor, rubberBandFillColor)


   def run(self, msgMapTool = False, msg = None):
      if self.plugIn.canvas.mapSettings().destinationCrs().isGeographic():
         self.showMsg(QadMsg.translate("QAD", "\nThe coordinate reference system of the project must be a projected coordinate system.\n"))
         return True # fine comando

      if self.virtualCmd == False: # se si vuole veramente salvare la polylinea in un layer   
         currLayer, errMsg = qad_layer.getCurrLayerEditable(self.plugIn.canvas, QgsWkbTypes.Polygon)
         if currLayer is None:
            self.showErr(errMsg)
            return True # fine comando

      #=========================================================================
      # RICHIESTA PRIMO PUNTO PER SELEZIONE OGGETTI
      if self.step == 0:
         self.PLINECommand = QadPLINECommandClass(self.plugIn, True)
         self.PLINECommand.setRubberBandColor(self.rubberBandBorderColor, self.rubberBandFillColor)
         # se questo flag = True il comando serve all'interno di un altro comando per disegnare una linea
         # che non verrà salvata su un layer
         self.PLINECommand.virtualCmd = True   
         self.PLINECommand.asToolForMPolygon = True # per rubberband tipo poligono
         self.PLINECommand.run(msgMapTool, msg)
         self.step = 1
         return False # continua     

      #=========================================================================
      # RISPOSTA ALLA RICHIESTA PUNTO (da step = 0 o 1)
      elif self.step == 1: # dopo aver atteso un punto si riavvia il comando
         if self.PLINECommand.run(msgMapTool, msg) == True:
            verticesLen = len(self.PLINECommand.vertices)
            if verticesLen >= 3:
               self.vertices = self.PLINECommand.vertices[:] # copio la lista
               firstVertex = self.vertices[0]
               # se l'ultimo vertice non é uguale al primo
               if self.vertices[verticesLen - 1] != firstVertex:
                  # aggiungo un vertice con le stesse coordinate del primo
                  self.vertices.append(firstVertex)
               if self.virtualCmd == False: # se si vuole veramente salvare la polylinea in un layer   
                  if qad_layer.addPolygonToLayer(self.plugIn, currLayer, self.vertices) == False:                     
                     self.showMsg(QadMsg.translate("Command_MPOLYGON", "\nPolygon not valid.\n"))
                     del self.vertices[:] # svuoto la lista
            else:
               self.showMsg(QadMsg.translate("Command_MPOLYGON", "\nPolygon not valid.\n"))
                               
            del self.PLINECommand
            self.PLINECommand = None
         
            return True # fine
            
         return False

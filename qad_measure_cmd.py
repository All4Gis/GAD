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
from .qad_entsel_cmd import QadEntSelClass
from .qad_getdist_cmd import QadGetDistClass
from .qad_textwindow import *
from .qad_entity import *
from .qad_variables import *
from . import qad_utils
from . import qad_layer
from .qad_dim import *


#===============================================================================
# QadMEASURECommandClassStepEnum class.
#===============================================================================
class QadMEASURECommandClassStepEnum():
   ASK_FOR_ENT        = 1 # richiede la selezione di un oggetto (0 è l'inizio del comando)
   ASK_FOR_ALIGNMENT  = 2 # richiede l'allineamento
   ASK_SEGMENT_LENGTH = 3 # richiede la lunghezza dei segmenti
   


# Classe che gestisce il comando MEASURE
class QadMEASURECommandClass(QadCommandClass):

   def instantiateNewCmd(self):
      """ istanzia un nuovo comando dello stesso tipo """
      return QadMEASURECommandClass(self.plugIn)
   
   def getName(self):
      return QadMsg.translate("Command_list", "MEASURE")

   def getEnglishName(self):
      return "MEASURE"

   def connectQAction(self, action):
      action.triggered.connect(self.plugIn.runMEASURECommand)

   def getIcon(self):
      return QIcon(":/plugins/qad/icons/measure.png")

   def getNote(self):
      # impostare le note esplicative del comando
      return QadMsg.translate("Command_MEASURE", "Creates punctual objects at measured intervals along the length or perimeter of an object.")
   
   def __init__(self, plugIn):
      QadCommandClass.__init__(self, plugIn)
      self.entSelClass = None
      self.GetDistClass = None
      self.objectAlignment = True
      self.segmentLength = 1

   def __del__(self):
      QadCommandClass.__del__(self)
      if self.entSelClass is not None:
         self.entSelClass.entity.deselectOnLayer()
         del self.entSelClass


   def getPointMapTool(self, drawMode = QadGetPointDrawModeEnum.NONE):
      if self.step == QadMEASURECommandClassStepEnum.ASK_SEGMENT_LENGTH: # quando si é in fase di richiesta distanza
         return self.GetDistClass.getPointMapTool()
      else:
         return QadCommandClass.getPointMapTool(self, drawMode)
      

   def getCurrentContextualMenu(self):
      if self.step == QadMEASURECommandClassStepEnum.ASK_SEGMENT_LENGTH: # quando si é in fase di richiesta distanza
         return self.GetDistClass.getCurrentContextualMenu()
      else:
         return self.contextualMenu


   #============================================================================
   # waitForEntsel
   #============================================================================
   def waitForEntsel(self, msgMapTool, msg):
      if self.entSelClass is not None:
         del self.entSelClass
      self.step = QadMEASURECommandClassStepEnum.ASK_FOR_ENT
      self.entSelClass = QadEntSelClass(self.plugIn)
      self.entSelClass.msg = QadMsg.translate("Command_MEASURE", "Select object to measure: ")
      # scarto la selezione di punti
      self.entSelClass.checkPointLayer = False
      self.entSelClass.checkLineLayer = True
      self.entSelClass.checkPolygonLayer = True
      self.entSelClass.checkDimLayers = False
      self.entSelClass.onlyEditableLayers = False

      self.entSelClass.run(msgMapTool, msg)


   #============================================================================
   # waitForAlignmentObjs
   #============================================================================
   def waitForAlignmentObjs(self):
      self.step = QadMEASURECommandClassStepEnum.ASK_FOR_ALIGNMENT

      keyWords = QadMsg.translate("QAD", "Yes") + "/" + QadMsg.translate("QAD", "No")
      self.defaultValue = QadMsg.translate("QAD", "Yes")
      prompt = QadMsg.translate("Command_MEASURE", "Align with object ? [{0}] <{1}>: ").format(keyWords, self.defaultValue)
      
      englishKeyWords = "Yes" + "/" + "No"
      keyWords += "_" + englishKeyWords

      # msg, inputType, default, keyWords, nessun controllo
      self.waitFor(prompt, \
                   QadInputTypeEnum.KEYWORDS, \
                   self.defaultValue, \
                   keyWords, QadInputModeEnum.NONE)

   
   #============================================================================
   # waitForSegmentLength
   #============================================================================
   def waitForSegmentLength(self):
      self.step = QadMEASURECommandClassStepEnum.ASK_SEGMENT_LENGTH
      
      if self.GetDistClass is not None:
         del self.GetDistClass
      self.GetDistClass = QadGetDistClass(self.plugIn)
      
      self.GetDistClass.msg = QadMsg.translate("Command_MEASURE", "Enter the length of segment: ")
      self.GetDistClass.run()


   #============================================================================
   # addFeature
   #============================================================================
   def addFeature(self, layer, insPt, rot):
      transformedPoint = self.mapToLayerCoordinates(layer, insPt)
      g = QgsGeometry.fromPoint(transformedPoint)
      f = QgsFeature()
      f.setGeometry(g)
      # Add attribute fields to feature.
      fields = layer.fields()
      f.setFields(fields)
      
      # assegno i valori di default
      provider = layer.dataProvider()
      for field in fields.toList():
         i = fields.indexFromName(field.name())
         f[field.name()] = provider.defaultValue(i)
      
      # se la scala dipende da un campo 
      scaleFldName = qad_layer.get_symbolScaleFieldName(layer)
      if len(scaleFldName) > 0:
         f.setAttribute(scaleFldName, 1.0)
      
      # se la rotazione dipende da un campo
      rotFldName = qad_layer.get_symbolRotationFieldName(layer)
      if len(rotFldName) > 0:
         f.setAttribute(rotFldName, qad_utils.toDegrees(rot))
      
      return qad_layer.addFeatureToLayer(self.plugIn, layer, f)               


   #============================================================================
   # doMeasure
   #============================================================================
   def doMeasure(self, dstLayer):
      f = self.entSelClass.entity.getFeature()
      if f is None:
         return
      
      layer = self.entSelClass.entity.layer
      
      # trasformo la geometria nel crs del canvas per lavorare con coordinate piane xy
      geom = self.layerToMapCoordinates(layer, f.geometry())
      
      # ritorna una tupla (<The squared cartesian distance>,
      #                    <minDistPoint>
      #                    <afterVertex>
      #                    <leftOf>)
      dummy = qad_utils.closestSegmentWithContext(self.entSelClass.point, geom)
      if dummy[2] is None:
         return False
      
      # ritorna la sotto-geometria al vertice <atVertex> e la sua posizione nella geometria (0-based)
      subGeom, atSubGeom = qad_utils.getSubGeomAtVertex(geom, dummy[2])
      pathLinearObjectList = qad_utils.QadLinearObjectList()
      geomType = subGeom.type()
      pathLinearObjectList.fromPolylineXY(subGeom.asPolyline())
      length = pathLinearObjectList.length()
      
      self.plugIn.beginEditCommand("Feature measured", dstLayer)
      
      i = 1
      distanceFromStart = self.segmentLength
      while distanceFromStart <= length:
         pt, rot = pathLinearObjectList.getPointFromStart(distanceFromStart)
         if self.addFeature(dstLayer, pt, rot if self.objectAlignment else 0) == False:
            self.plugIn.destroyEditCommand()
            return False
         i = i + 1
         distanceFromStart = distanceFromStart + self.segmentLength 

      self.plugIn.endEditCommand()
      return True

   def run(self, msgMapTool = False, msg = None):
      if self.plugIn.canvas.mapSettings().destinationCrs().isGeographic():
         self.showMsg(QadMsg.translate("QAD", "\nThe coordinate reference system of the project must be a projected coordinate system.\n"))
         return True # fine comando
      
      currLayer, errMsg = qad_layer.getCurrLayerEditable(self.plugIn.canvas, QgsWkbTypes.Point)
      if currLayer is None:
         self.showErr(errMsg)
         return True # fine comando

      if qad_layer.isSymbolLayer(currLayer) == False :
         errMsg = QadMsg.translate("QAD", "\nCurrent layer is not a symbol layer.")
         errMsg = errMsg + QadMsg.translate("QAD", "\nA symbol layer is a vector punctual layer without label.\n")
         self.showErr(errMsg)
         return True # fine comando
      
      if  len(QadDimStyles.getDimListByLayer(currLayer)) > 0:
         errMsg = QadMsg.translate("QAD", "\nThe current layer belongs to a dimension style.\n")
         self.showErr(errMsg)
         return True # fine comando

      if self.step == 0:     
         self.waitForEntsel(msgMapTool, msg)
         return False # continua


      #=========================================================================
      # RISPOSTA ALLA SELEZIONE DI UN'ENTITA' (da step = 0)
      elif self.step == QadMEASURECommandClassStepEnum.ASK_FOR_ENT:
         if self.entSelClass.run(msgMapTool, msg) == True:
            if self.entSelClass.entity.isInitialized():
               # se il layer di destinazione è di tipo simbolo
               if qad_layer.isSymbolLayer(currLayer) == True:
                  # se il simbolo può essere ruotato
                  if len(qad_layer.get_symbolRotationFieldName(currLayer)) >0:
                     self.waitForAlignmentObjs()
                  else:
                     self.waitForSegmentLength()
               return False
            else:
               if self.entSelClass.canceledByUsr == True: # fine comando
                  return True
               self.showMsg(QadMsg.translate("QAD", "No geometries in this position."))
               self.waitForEntsel(msgMapTool, msg)
         return False # continua
      

      #=========================================================================
      # RISPOSTA ALLA RICHIESTA DI ALLINEARE GLI OGGETTI (da step = ASK_FOR_ENT)
      elif self.step == QadMEASURECommandClassStepEnum.ASK_FOR_ALIGNMENT: # dopo aver atteso una parola chiave si riavvia il comando
         if msgMapTool == True: # il punto arriva da una selezione grafica
            if self.getPointMapTool().rightButton == True: # se usato il tasto destro del mouse
               value = self.defaultValue 
            else:
               self.setMapTool(self.getPointMapTool()) # riattivo il maptool
               return False
         else:
            # la parola chiave arriva come parametro della funzione
            value = msg

         if type(value) == unicode:
            if value == QadMsg.translate("QAD", "Yes") or value == "Yes":
               self.objectAlignment = True
            else:
               self.objectAlignment = False

            self.waitForSegmentLength()
         
         return False 


      #=========================================================================
      # RISPOSTA ALLA RICHIESTA DELLA LUNGHEZZA DEL SEGMENTO (da step = ASK_FOR_ALIGNMENT)
      #=========================================================================
      elif self.step == QadMEASURECommandClassStepEnum.ASK_SEGMENT_LENGTH: # dopo aver atteso un numero reale si riavvia il comando
         if self.GetDistClass.run(msgMapTool, msg) == True:
            self.getPointMapTool().refreshSnapType() # aggiorno lo snapType che può essere variato da altri maptool
            if self.GetDistClass.dist is not None:
               self.segmentLength = self.GetDistClass.dist
               self.doMeasure(currLayer)

            del self.GetDistClass
            return True # fine comando
         else:
            return False
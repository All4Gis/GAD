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
from qgis.gui import *
import re # regular expression


from .qad_msg import QadMsg
from . import qad_utils




#===============================================================================
# layerGeometryTypeToStr
#===============================================================================
def layerGeometryTypeToStr(geomType):
   """
   restituisce la stringa corrispondente al tipo di geometria del layer
   """
   msg = ""
   if (type(geomType) == list or type(geomType) == tuple): # se lista di tipi
      for gType in geomType:
         if len(msg) > 0:
            msg = msg + ", " 
         msg = msg + layerGeometryTypeToStr(gType)
   else:
      if geomType == QgsWkbTypes.Point:
         msg = QadMsg.translate("QAD", "point") 
      elif geomType == QgsWkbTypes.LineString:
         msg = QadMsg.translate("QAD", "line") 
      elif geomType == QgsWkbTypes.Polygon:
         msg = QadMsg.translate("QAD", "polygon") 

   return msg


#===============================================================================
# getCurrLayerEditable
#===============================================================================
def getCurrLayerEditable(canvas, geomType = None):
   """
   Ritorna il layer corrente se é aggiornabile e compatibile con il tipo geomType +
   eventuale messaggio di errore.
   Se <geomType> é una lista allora verifica che sia compatibile con almeno un tipo nella lista <geomType>
   altrimenti se <> None verifica che sia compatibile con il tipo <geomType>
   """
   vLayer = canvas.currentLayer()
   if vLayer is None:
      return None, QadMsg.translate("QAD", "\nNo current layer.\n")
   
   if (vLayer.type() != QgsMapLayer.VectorLayer):
      return None, QadMsg.translate("QAD", "\nThe current layer is not a vector layer.\n")

   if geomType is not None:
      if (type(geomType) == list or type(geomType) == tuple): # se lista di tipi
         if vLayer.geometryType() not in geomType:
            errMsg = QadMsg.translate("QAD", "\nThe geometry type of the current layer is {0} and it is not valid.\n")
            errMsg = errMsg + QadMsg.translate("QAD", "Admitted {1} layer type only.\n")
            errMsg.format(layerGeometryTypeToStr(vLayer.geometryType()), layerGeometryTypeToStr(geomType))
            return None, errMsg.format(layerGeometryTypeToStr(vLayer.geometryType()), layerGeometryTypeToStr(geomType))
      else:
         if vLayer.geometryType() != geomType:
            errMsg = QadMsg.translate("QAD", "\nThe geometry type of the current layer is {0} and it is not valid.\n")
            errMsg = errMsg + QadMsg.translate("QAD", "Admitted {1} layer type only.\n")
            errMsg.format(layerGeometryTypeToStr(vLayer.geometryType()), layerGeometryTypeToStr(geomType))
            return None, errMsg.format(layerGeometryTypeToStr(vLayer.geometryType()), layerGeometryTypeToStr(geomType))

   provider = vLayer.dataProvider()
   if not (provider.capabilities() & QgsVectorDataProvider.EditingCapabilities):
      return None, QadMsg.translate("QAD", "\nThe current layer is not editable.\n")
   
   if not vLayer.isEditable():
      return None, QadMsg.translate("QAD", "\nThe current layer is not editable.\n")

   return vLayer, None
  

#===============================================================================
# addPointToLayer
#===============================================================================
def addPointToLayer(plugIn, layer, point, transform = True, refresh = True, check_validity = False):
   """
   Aggiunge un punto ad un layer. Se il punto é già 
   nel sistema di coordinate del layer allora non va trasformato se invece é nel
   sistema map-coordinate allora transform deve essere = True
   """
   if len(points) < 2:
      return False
     
   f = QgsFeature()
   
   if transform:
      transformedPoint = plugIn.canvas.mapSettings().mapToLayerCoordinates(layer, point)
      g = QgsGeometry.fromPointXY(transformedPoint)
   else:
      g = QgsGeometry.fromPointXY(point)

   if check_validity:
      if not g.isGeosValid():
         return False
      
   f.setGeometry(g)
   
   # Add attributefields to feature.
   fields = layer.fields()
   f.setFields(fields)

   # assegno i valori di default
   provider = layer.dataProvider()
   for field in fields.toList():
      i = fields.indexFromName(field.name())
      f[field.name()] = provider.defaultValue(i)

   if refresh == True:
      plugIn.beginEditCommand("Feature added", layer)

   if layer.addFeature(f, False):
      if refresh == True:
         plugIn.endEditCommand()
      plugIn.setLastEntity(layer, f.id())
      result = True
   else:
      if refresh == True:
         plugIn.destroyEditCommand()
      result = False
      
   return result


#===============================================================================
# addLineToLayer
#===============================================================================
def addLineToLayer(plugIn, layer, points, transform = True, refresh = True, check_validity = False):
   """
   Aggiunge una linea (lista di punti) ad un layer. Se la lista di punti é già 
   nel sistema di coordinate del layer allora non va trasformata se invece é nel
   sistema  map-coordinate allora transform deve essere = True
   """
   if len(points) < 2: # almeno 2 punti
      return False
     
   f = QgsFeature()
   
   if transform:
      layerPoints = []
      for point in points:
         transformedPoint = plugIn.canvas.mapSettings().mapToLayerCoordinates(layer, point)
         layerPoints.append(transformedPoint)    
      g = QgsGeometry.fromPolylineXY(layerPoints)
   else:
      g = QgsGeometry.fromPolylineXY(points)

   if check_validity:
      if not g.isGeosValid():
         return False
      
   f.setGeometry(g)
   
   # Add attributefields to feature.
   fields = layer.fields()
   f.setFields(fields)

   # assegno i valori di default
   provider = layer.dataProvider()
   for field in fields.toList():
      i = fields.indexFromName(field.name())
      f[field.name()] = provider.defaultValue(i)

   if refresh == True:
      plugIn.beginEditCommand("Feature added", layer)

   if layer.addFeature(f):
      if refresh == True:
         plugIn.endEditCommand()
      plugIn.setLastEntity(layer, f.id())
      result = True
   else:
      if refresh == True:
         plugIn.destroyEditCommand()
      result = False
      
   return result


#===============================================================================
# addPolygonToLayer
#===============================================================================
def addPolygonToLayer(plugIn, layer, points, transform = True, refresh = True, check_validity = False):
   """
   Aggiunge un poligono (lista di punti) ad un layer. Se la lista di punti é già 
   nel sistema di coordinate del layer allora non va trasformata se invece é nel
   sistema  map-coordinate allora transform deve essere = True
   """
   if len(points) < 3: # almeno 4 punti (il primo e l'ultimo sono uguali)
      return False
     
   f = QgsFeature()
   
   if transform:
      layerPoints = []
      for point in points:
         transformedPoint = plugIn.canvas.mapSettings().mapToLayerCoordinates(layer, point)
         layerPoints.append(transformedPoint)      
      g = QgsGeometry.fromPolygonXY([layerPoints])
   else:
      g = QgsGeometry.fromPolygonXY([points])

   if check_validity:
      if not g.isGeosValid():
         return False
         
   f.setGeometry(g)
   
   # Add attributefields to feature.
   fields = layer.fields()
   f.setFields(fields)

   # assegno i valori di default
   provider = layer.dataProvider()
   for field in fields.toList():
      i = fields.indexFromName(field.name())
      f[field.name()] = provider.defaultValue(i)

   if refresh == True:
      plugIn.beginEditCommand("Feature added", layer)

   if layer.addFeature(f, False):
      if refresh == True:
         plugIn.endEditCommand()
      plugIn.setLastEntity(layer, f.id())
      result = True
   else:
      if refresh == True:
         plugIn.destroyEditCommand()
      result = False
      
   return result


#===============================================================================
# addGeomToLayer
#===============================================================================
def addGeomToLayer(plugIn, layer, geom, coordTransform = None, refresh = True, check_validity = False):
   """
   Aggiunge una geometria ad un layer. Se la geometria é da convertire allora
   deve essere passato il parametro <coordTransform> di tipo QgsCoordinateTransform.
   refresh controlla la transazione del comando e il refresh del canvas
   """     
   f = QgsFeature()
   
   g = QgsGeometry(geom)
   if coordTransform is not None:
      g.transform(coordTransform)            

   if check_validity:
      if not g.isGeosValid():
         return False
      
   f.setGeometry(g)
   
   # Add attributefields to feature.
   fields = layer.fields()
   f.setFields(fields)

   # assegno i valori di default
   provider = layer.dataProvider()
   for field in fields.toList():
      i = fields.indexFromName(field.name())
      f[field.name()] = provider.defaultValue(i)

   if refresh == True:
      plugIn.beginEditCommand("Feature added", layer)

   if layer.addFeature(f, False):
      if refresh == True:
         plugIn.endEditCommand()
      plugIn.setLastEntity(layer, f.id())
      result = True
   else:
      if refresh == True:
         plugIn.destroyEditCommand()
      result = False
      
   return result


#===============================================================================
# addGeomsToLayer
#===============================================================================
def addGeomsToLayer(plugIn, layer, geoms, coordTransform = None, refresh = True, check_validity = False):
   """
   Aggiunge le geometrie ad un layer. Se la geometria é da convertire allora
   deve essere passato il parametro <coordTransform> di tipo QgsCoordinateTransform.
   refresh controlla la transazione del comando e il refresh del canvas
   """
   if refresh == True:
      plugIn.beginEditCommand("Feature added", layer)
      
   for geom in geoms:
      if addGeomToLayer(plugIn, layer, geom, coordTransform, False, check_validity) == False:
         if refresh == True:
            plugIn.destroyEditCommand()
            return False
         
   if refresh == True:
      plugIn.endEditCommand()

   return True


#===============================================================================
# addFeatureToLayer
#===============================================================================
def addFeatureToLayer(plugIn, layer, f, coordTransform = None, refresh = True, check_validity = False):
   """
   Aggiunge una feature ad un layer. Se la geometria é da convertire allora
   deve essere passato il parametro <coordTransform> di tipo QgsCoordinateTransform.
   <refresh> controlla la transazione del comando e il refresh del canvas
   """     
   
   if coordTransform is not None:
      g = QgsGeometry(f.geometry())
      g.transform(coordTransform)            
      f.setGeometry(g)

   if check_validity:
      if not f.geometry().isGeosValid():
         return False
         
   if refresh == True:
      plugIn.beginEditCommand("Feature added", layer)

   # use default value for primary key fields if it's NOT NULL
   provider = layer.dataProvider()
   pkAttrList = layer.primaryKeyAttributes()
   count = layer.fields().count()
   i = 0
   while i < count:
      if i in pkAttrList:
         defVal = provider.defaultValue(i)
         if not isinstance(defVal, QPyNullVariant) or layer.providerType() == "spatialite":
            f[i] = provider.defaultValue(i)         
      i = i + 1
 
   if layer.addFeature(f):
      if refresh == True:
         plugIn.endEditCommand()
         
      plugIn.setLastEntity(layer, f.id())
      result = True
   else:
      if refresh == True:
         plugIn.destroyEditCommand()
      result = False
      
   return result


#===============================================================================
# addFeaturesToLayer
#===============================================================================
def addFeaturesToLayer(plugIn, layer, features, coordTransform = None, refresh = True, check_validity = False):
   """
   Aggiunge le feature ad un layer. Se la geometria é da convertire allora
   deve essere passato il parametro <coordTransform> di tipo QgsCoordinateTransform.
   <refresh> controlla la transazione del comando e il refresh del canvas
   """
   if refresh == True:
      plugIn.beginEditCommand("Feature added", layer)
      
   for f in features:
      if addFeatureToLayer(plugIn, layer, f, coordTransform, False, check_validity) == False:
         if refresh == True:
            plugIn.destroyEditCommand()
            return False
         
   if refresh == True:
      plugIn.endEditCommand()
   
   return True


#===============================================================================
# updateFeatureToLayer
#===============================================================================
def updateFeatureToLayer(plugIn, layer, f, refresh = True, check_validity = False):
   """
   Aggiorna la feature ad un layer.
   refresh controlla la transazione del comando e il refresh del canvas
   """        
   if check_validity:
      if not f.geometry().isGeosValid():
         return False
      
   if refresh == True:
      plugIn.beginEditCommand("Feature modified", layer)

   if layer.updateFeature(f):
      if refresh == True:
         plugIn.endEditCommand()
         
      result = True
   else:
      if refresh == True:
         plugIn.destroyEditCommand()
      result = False
      
   return result


#===============================================================================
# updateFeaturesToLayer
#===============================================================================
def updateFeaturesToLayer(plugIn, layer, features, refresh = True, check_validity = False):
   """
   Aggiorna le features ad un layer.
   refresh controlla la transazione del comando e il refresh del canvas
   """
   if refresh == True:
      plugIn.beginEditCommand("Feature modified", layer)
      
   for f in features:
      if updateFeatureToLayer(plugIn, layer, f, False, check_validity) == False:
         if refresh == True:
            plugIn.destroyEditCommand()
            return False
         
   if refresh == True:
      plugIn.endEditCommand()
   
   return True


#===============================================================================
# deleteFeatureToLayer
#===============================================================================
def deleteFeatureToLayer(plugIn, layer, featureId, refresh = True):
   """
   Cancella la feature da un layer.
   refresh controlla la transazione del comando e il refresh del canvas
   """        
   if refresh == True:
      plugIn.beginEditCommand("Feature deleted", layer)

   if layer.deleteFeature(featureId):
      if refresh == True:
         plugIn.endEditCommand()
         
      result = True
   else:
      if refresh == True:
         plugIn.destroyEditCommand()
      result = False
      
   return result


#===============================================================================
# deleteFeaturesToLayer
#===============================================================================
def deleteFeaturesToLayer(plugIn, layer, featureIds, refresh = True):
   """
   Aggiorna le features ad un layer.
   refresh controlla la transazione del comando e il refresh del canvas
   """
   if refresh == True:
      plugIn.beginEditCommand("Feature deleted", layer)
      
   for featureId in featureIds:
      if deleteFeatureToLayer(plugIn, layer, featureId, False) == False:
         if refresh == True:
            plugIn.destroyEditCommand()
            return False
         
   if refresh == True:
      plugIn.endEditCommand()
   
   return True


#===============================================================================
# getLayersByName
#===============================================================================
def getLayersByName(regularExprName):
   """
   Ritorna la lista dei layer il cui nome soddisfa la regular expression di ricerca
   (per conversione da wildcards vedi la funzione wildCard2regularExpr)
   the regular expression to only match if the text is an exact match is
   (for example, to match for abc, then 1abc1, 1abc, and abc1 would not match):
   use the start and end delimiters: ^abc$
   """
   result = []
   regExprCompiled = re.compile(regularExprName)
   for layer in QgsProject.instance().mapLayers().values():
      if re.match(regExprCompiled, layer.name()):
         if layer.isValid():
            result.append(layer)

   return result


#===============================================================================
# getLayerById
#===============================================================================
def getLayerById(id):
   """
   Ritorna il layer con id noto
   """
   for layer in QgsProject.instance().mapLayers().values():
      if layer.id() == id:
         return layer
   return None


#===============================================================================
# get_symbolRotationFieldName
#===============================================================================
def get_symbolRotationFieldName(layer):
   """
   return rotation field name (or empty string if not set or not supported by renderer) 
   """
   if (layer.type() != QgsMapLayer.VectorLayer) or (layer.geometryType() != QgsWkbTypes.Point):
      return ""

   try:
      expr = QgsSymbolLayerV2Utils.fieldOrExpressionToExpression(layer.rendererV2().rotationField())
      columns = expr.referencedColumns()
      return columns[0] if len(columns) == 1 else ""
   except:
      return ""


#===============================================================================
# get_symbolScaleFieldName
#===============================================================================
def get_symbolScaleFieldName(layer):
   """
   return symbol scale field name (or empty string if not set or not supported by renderer) 
   """
   if (layer.type() != QgsMapLayer.VectorLayer) or (layer.geometryType() != QgsWkbTypes.Point):
      return ""
   
   try:
      expr = QgsSymbolLayerV2Utils.fieldOrExpressionToExpression(layer.rendererV2().sizeScaleField())
      columns = expr.referencedColumns()
      return columns[0] if len(columns) == 1 else ""
   except:
      return ""
   


#===============================================================================
# isTextLayer
# Description: Check if it has label configured. A Text layer it's a layer that is
# field selected for labeling and not a dynamic layer
#===============================================================================
def isTextLayer(layer):
   labeling = layer.labeling()
   fields = layer.fields()
   if labeling:#If labeling options actif
      label = labeling.settings()
      if not label.isExpression: #If not an expression
         field = label.fieldName
         if fields.field(field): #if its a field only for labeling
            return True
   return False


#===============================================================================
# isSymbolLayer
# Description: Check if it is a symbol layer. A Symbol layer it's a layer that is
# vectorial and has a point geometry type
#===============================================================================
def isSymbolLayer(layer):
   if (layer.type() != QgsMapLayer.VectorLayer) or (layer.geometryType() != QgsWkbTypes.PointGeometry):
      return False
   return True


#===============================================================================
# createQADTempLayer
#===============================================================================
def createQADTempLayer(plugIn, GeomType):
   """
   Aggiunge tre liste di geometrie rispettivamente a tre layer temporanei di QAD (uno per tipologia di
   geometria). Se le geometrie sono da convertire allora
   deve essere passato il parametro <coordTransform> di tipo QgsCoordinateTransform.
   <epsg> = the authority identifier for this srs    
   """
   layer = None
   epsg = plugIn.iface.mapCanvas().mapSettings().destinationCrs().authid()
   
   if GeomType == QgsWkbTypes.Point:
      layerName = QadMsg.translate("QAD", "QAD - Temporary points")
      layerList = QgsProject.instance().mapLayersByName(layerName)
      if len(layerList) == 0:
         layer = QgsVectorLayer("Point?crs=%s&index=yes" % epsg, layerName, "memory")
         QgsProject.instance().addMapLayers([layer], True)
      else:
         layer = layerList[0]
   elif GeomType == QgsWkbTypes.LineString:
      layerName = QadMsg.translate("QAD", "QAD - Temporary lines") 
      layerList = QgsProject.instance().mapLayersByName(layerName)
      if len(layerList) == 0:
         layer = QgsVectorLayer("LineString?crs=%s&index=yes" % epsg, layerName, "memory")
         QgsProject.instance().addMapLayers([layer], True)
      else:
         layer = layerList[0]
   elif GeomType == QgsWkbTypes.Polygon:
      layerName = QadMsg.translate("QAD", "QAD - Temporary polygons") 
      layerList = QgsProject.instance().mapLayersByName(layerName)
      if len(layerList) == 0:
         layer = QgsVectorLayer("Polygon?crs=%s&index=yes" % epsg, layerName, "memory")
         QgsProject.instance().addMapLayers([layer], True)
      else:
         layer = layerList[0]

   layer.startEditing()
   return layer

   
#===============================================================================
# addGeometriesToQADTempLayers
#===============================================================================
def addGeometriesToQADTempLayers(plugIn, pointGeoms = None, lineGeoms = None, polygonGeoms = None, \
                               crs = None, refresh = True):
   """
   Aggiunge tre liste di geometrie rispettivamente a tre layer temporanei di QAD (uno per tipologia di
   geometria). Se le geometrie sono da convertire allora
   deve essere passato il parametro <csr> che definisce il sistema di coordinate delle geometrie.
   """   
   if pointGeoms is not None and len(pointGeoms) > 0:
      layer = createQADTempLayer(plugIn, QgsWkbTypes.Point)
      if layer is None:
         return False
      if crs is None:
         # plugIn, layer, geoms, coordTransform , refresh, check_validity
         if addGeomsToLayer(plugIn, layer, pointGeoms, None, refresh, False) == False:
            return False
      else:
         # plugIn, layer, geoms, coordTransform , refresh, check_validity
         if addGeomsToLayer(plugIn, layer, pointGeoms, QgsCoordinateTransform(crs, layer.crs(),QgsProject.instance()), \
                            refresh, False) == False:
            return False
      
   if lineGeoms is not None and len(lineGeoms) > 0:
      layer = createQADTempLayer(plugIn, QgsWkbTypes.LineString)
      if layer is None:
         return False
      if crs is None:
         # plugIn, layer, geoms, coordTransform , refresh, check_validity
         if addGeomsToLayer(plugIn, layer, lineGeoms, None, refresh, False) == False:
            return False
      else:
         # plugIn, layer, geoms, coordTransform , refresh, check_validity
         if addGeomsToLayer(plugIn, layer, lineGeoms, QgsCoordinateTransform(crs, layer.crs(),QgsProject.instance()), \
                            refresh, False) == False:
            return False
      
   if polygonGeoms is not None and len(polygonGeoms) > 0:
      layer = createQADTempLayer(plugIn, QgsWkbTypes.Polygon)
      if layer is None:
         return False
      if crs is None:
         # plugIn, layer, geoms, coordTransform , refresh, check_validity
         if addGeomsToLayer(plugIn, layer, polygonGeoms, None, refresh, False) == False:
            return False
      else:
         # plugIn, layer, geoms, coordTransform , refresh, check_validity
         if addGeomsToLayer(plugIn, layer, polygonGeoms, QgsCoordinateTransform(crs, layer.crs(),QgsProject.instance()), \
                            refresh, False) == False:
            return False
        
   return True


#===============================================================================
# QadLayerStatusEnum class.
#===============================================================================
class QadLayerStatusEnum():
   UNKNOWN = 0
   COMMIT_BY_EXTERNAL = 1 # salvataggio quando questo è richiamato da eventi esterni a QAD
   COMMIT_BY_INTERNAL = 2 # salvataggio quando questo è richiamato da eventi interni a QAD

#===============================================================================
# QadLayerStatusListClass class.
#===============================================================================
class QadLayerStatusListClass():
   def __init__(self):
      self.layerStatusList = [] # lista di coppie (<id layer>-<stato layer>)

   def __del__(self):
      del self.layerStatusList

   def getStatus(self, layerId):
      for layerStatus in self.layerStatusList:
         if layerStatus[0] == layerId:
            return layerStatus[1]
      return QadLayerStatusEnum.UNKNOWN
   
   def setStatus(self, layerId, status):
      # verifico se c'era già in lista
      for layerStatus in self.layerStatusList:
         if layerStatus[0] == layerId:
            layerStatus[1] = status
            return
      # se non c'era lo aggiungo
      self.layerStatusList.append([layerId, status])
      return
   
   def remove(self, layerId):
      i = 0
      for layerStatus in self.layerStatusList:
         if layerStatus[0] == layerId:
            del self.layerStatusList[i]
            return
         else:
            i = i + 1
      return
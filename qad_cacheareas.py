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



from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *


#===============================================================================
# QadLayerCacheGeoms class.
#===============================================================================
class QadLayerCacheGeoms():
   """
   Classe che gestisce la cache delle geometrie di un layer
   """
      
   
   #============================================================================
   # __init__
   #============================================================================
   def __init__(self, layer):
      self.layer = layer
      self.cacheLayer = None
      self.IsEmpty = True
      # creo un layer temporaneo in memoria
      self.__create_internal_layer()

      self.layer.featureAdded.connect(self.onFeatureAdded)
      self.layer.featureDeleted.connect(self.onFeatureDeleted)
      self.layer.geometryChanged.connect(self.onGeometryChanged)


   def __create_internal_layer(self):
      if self.cacheLayer is not None:
         del self.cacheLayer
      
      str = getStrLayerGeomType(self.layer)
      str = str + "?crs="
      #str = str + self.layer.crs().authid()
      str = str + self.layer.crs().toWkt()
      str = str + "&index=yes"
      # creo un layer temporaneo in memoria
      self.cacheLayer = QgsVectorLayer(str, "QadLayerCacheArea", "memory")
      provider = self.cacheLayer.dataProvider()
      provider.addAttributes([QgsField("index", QVariant.Int, "Int")])
      self.cacheLayer.updateFields()
      
      if provider.capabilities() & QgsVectorDataProvider.CreateSpatialIndex:
         provider.createSpatialIndex()

   
   #============================================================================
   # __del__
   #============================================================================
   def __del__(self):
      del self.cacheLayer
      self.layer.featureAdded.disconnect(self.onFeatureAdded)
      self.layer.featureDeleted.disconnect(self.onFeatureDeleted)
      self.layer.geometryChanged.disconnect(self.onGeometryChanged)


   #============================================================================
   # insertFeature
   #============================================================================
   def insertFeature(self, feature):
      # inserisce questa feature nella cache
      if self.cacheLayer.startEditing() == False:
         return False
      
      geom = feature.geometry()
      if geom is None:
         return
      newFeature = QgsFeature()
      newFeature.initAttributes(1)
      newFeature.setAttribute(0, feature.id())
      newFeature.setGeometry(geom)
      if self.cacheLayer.addFeature(newFeature):
         if self.cacheLayer.commitChanges():
            self.IsEmpty = False
            return True
         else:
            return False
      else:
         self.cacheLayer.rollBack()
         return False


   #============================================================================
   # insertFeatures
   #============================================================================
   def insertFeatures(self, features):
      if len(features) == 0:
         return
      
      # inserisce questa feature nella cache
      if self.cacheLayer.startEditing() == False:
         return False

      newFeature = QgsFeature()
      newFeature.initAttributes(1)
      
      for feature in features:
         geom = feature.geometry()
         if geom is None:
            continue
         newFeature.setAttribute(0, feature.id())
         newFeature.setGeometry(geom)
         if self.cacheLayer.addFeature(newFeature) == False:
            self.cacheLayer.rollBack()
            return False

      
      if self.cacheLayer.commitChanges():
         self.IsEmpty = False
         return True
      else:
         self.cacheLayer.rollBack()
         return False


   #============================================================================
   # __deleteFeature
   #============================================================================
   def __deleteFeature(self, fid):
      # inserisce questa feature nella cache
      if self.cacheLayer.startEditing() == False:
         return False

      if self.cacheLayer.deleteFeature(fid):
         return self.cacheLayer.commitChanges()
      else:
         self.cacheLayer.rollBack()
         return False


   #============================================================================
   # __updateFeature
   #============================================================================
   def __updateFeature(self, fid, geom):
      feature = QgsFeature()
      if self.cacheLayer.getFeatures(QgsFeatureRequest().setFilterFid(fid)).nextFeature(feature):
         # aggiorna la geometria di questa feature nella cache
         feature.setGeometry(geom)

         if self.cacheLayer.startEditing() == False:
            return False
         
         if self.cacheLayer.updateFeature(feature):
            return self.cacheLayer.commitChanges()
         else:
            self.cacheLayer.rollBack()
      
      return False


   #============================================================================
   # getFeatures
   #============================================================================
   def getFeatures(self, rect):
      if self.IsEmpty:
         return []
      feature = QgsFeature()
      featureList = []
      featureIterator = self.cacheLayer.getFeatures(getFeatureRequest(rect, True))
      for feature in featureIterator:
         featureList.append(QgsFeature(feature))
      
      return featureList


   #============================================================================
   # extent
   #============================================================================
   def extent(self, rect):
      return self.cacheLayer.extent()


   #============================================================================
   # onFeatureAdded
   #============================================================================
   def onFeatureAdded(self, fid):
      feature = QgsFeature()
      if self.layer.getFeatures(QgsFeatureRequest().setFilterFid(fid)).nextFeature(feature):
         return self.insertFeature(feature)
      return False
   
   
   #============================================================================
   # onFeatureDeleted
   #============================================================================
   def onFeatureDeleted(self, fid):
      feature = QgsFeature()
      if self.cacheLayer.getFeatures(QgsFeatureRequest().setFilterExpression("\"index\"=" + str(fid))).nextFeature(feature):
         return self.__deleteFeature(feature.id())
      return False


   #============================================================================
   # onGeometryChanged
   #============================================================================
   def onGeometryChanged(self, fid, geom):
      feature = QgsFeature()
      if self.cacheLayer.getFeatures(QgsFeatureRequest().setFilterFid(fid)).nextFeature(feature):
         return self.__updateFeature(feature.id(), geom)
      
      return False


#===============================================================================
# QadLayerCacheGeomsDict class.
#===============================================================================
class QadLayerCacheGeomsDict():
   """
   Classe che gestisce un dizionario delle chache delle geometrie dei layer
   """


   #============================================================================
   # __init__
   #============================================================================
   def __init__(self, canvas = None):
      self.canvas = canvas
      
      self.layersToCheck = None
      self.checkPointLayer = True
      self.checkLineLayer = True
      self.checkPolygonLayer = True
      self.onlyEditableLayers = False
      
      self.layerCacheAreaDict = dict() # dizionario delle chache delle aree dei layer
      if self.canvas is not None:
         self.canvas.extentsChanged.connect(self.onExtentsChanged)
         self.canvas.layersChanged.connect(self.onLayersChanged)
         #self.canvas.layerStyleOverridesChanged.connect(self.onLayerStyleOverridesChanged) da qgis 2.12

   
   #============================================================================
   # __del__
   #============================================================================
   def __del__(self):
      del self.layerCacheAreaDict
      if self.canvas is not None:
         self.canvas.extentsChanged.disconnect(self.onExtentsChanged)
         self.canvas.layersChanged.disconnect(self.onLayersChanged)
         # self.canvas.layerStyleOverridesChanged.disconnect(self.onLayerStyleOverridesChanged) da qgis 2.12


   #============================================================================
   # insertFeature
   #============================================================================
   def insertFeature(self, layer, feature):
      # inserisce questa feature nella cache
      layerId = layer.id()
      # verifica se layer esiste già nel dizionario
      if layerId not in self.layerCacheAreaDict:
         cacheArea = QadLayerCacheGeoms(layer)
         self.layerCacheAreaDict[layerId] = cacheArea
      else:
         cacheArea = self.layerCacheAreaDict[layerId]
      cacheArea.insertFeature(feature)


   #============================================================================
   # insertFeatures
   #============================================================================
   def insertFeatures(self, layer, features):
      if len(features) == 0:
         return
      # inserisce questa feature nella cache
      layerId = layer.id()
      # verifica se layer esiste già nel dizionario
      if layerId not in self.layerCacheAreaDict:
         cacheArea = QadLayerCacheGeoms(layer)
         self.layerCacheAreaDict[layerId] = cacheArea
      else:
         cacheArea = self.layerCacheAreaDict[layerId]
      cacheArea.insertFeatures(features)


   #============================================================================
   # refreshOnMapCanvasExtent
   #============================================================================
   def refreshOnMapCanvasExtent(self, layersToCheck = None, \
                                checkPointLayer = True, checkLineLayer = True, checkPolygonLayer = True, \
                                onlyEditableLayers = False):
      """
      la funzione aggiorna la cache usando l'estensione dello schermo corrente.
      layersToCheck = opzionale, lista dei layer in cui cercare
      checkPointLayer = opzionale, considera i layer di tipo punto
      checkLineLayer = opzionale, considera i layer di tipo linea
      checkPolygonLayer = opzionale, considera i layer di tipo poligono
      onlyEditableLayers = per cercare solo nei layer modificabili
      """
      if self.canvas is None:
         return
      
      self.layersToCheck = layersToCheck
      self.checkPointLayer = checkPointLayer
      self.checkLineLayer = checkLineLayer
      self.checkPolygonLayer = checkPolygonLayer
      self.onlyEditableLayers = onlyEditableLayers
      
      if checkPointLayer == False and checkLineLayer == False and checkPolygonLayer == False:
         return

      boundBox = self.canvas.extent() # in map coordinate

      if layersToCheck is None:
         # Tutti i layer visibili
         _layers = self.canvas.layers()
      else:
         # solo la lista passata come parametro
         _layers = layersToCheck
      
      for layer in _layers: # ciclo sui layer
         # considero solo i layer vettoriali che sono filtrati per tipo
         if (layer.type() == QgsMapLayer.VectorLayer) and \
             ((layer.geometryType() == QgsWkbTypes.PointGeometry and checkPointLayer == True) or \
              (layer.geometryType() == QgsWkbTypes.LineGeometry and checkLineLayer == True) or \
              (layer.geometryType() == QgsWkbTypes.PolygonGeometry and checkPolygonLayer == True)) and \
              (onlyEditableLayers == False or layer.isEditable()):                      

            # se il layer non è visibile a questa scala
            if layer.hasScaleBasedVisibility() and \
               (self.canvas.mapSettings().scale() < layer.minimumScale() or self.canvas.mapSettings().scale() > layer.maximumScale()):
               continue

            rect = self.canvas.mapSettings().mapToLayerCoordinates(layer, boundBox) # map to layer coordinate
               
            self.refreshOnRectOnLayer(layer, rect)


   #===============================================================================
   # refreshOnRectOnLayer
   #===============================================================================
   def refreshOnRectOnLayer(self, layer, rect):
      featureList = []
      featureIterator = layer.getFeatures(getFeatureRequest(rect, False))
      feature = QgsFeature()
      for feature in featureIterator:
         featureList.append(QgsFeature(feature))
   
      # non ho trovato oggetti quindi lo segno in cache
      return self.insertFeatures(layer, featureList)

   
   #============================================================================
   # onExtentsChanged
   #============================================================================
   def onExtentsChanged(self):
      self.refreshOnMapCanvasExtent(self.layersToCheck, \
                                    self.checkPointLayer, self.checkLineLayer, self.checkPolygonLayer, \
                                    self.onlyEditableLayers)


   #============================================================================
   # onLayersChanged
   #============================================================================
   def onLayersChanged(self):
      self.refreshOnMapCanvasExtent(self.layersToCheck, \
                                    self.checkPointLayer, self.checkLineLayer, self.checkPolygonLayer, \
                                    self.onlyEditableLayers)


   #============================================================================
   # onLayerStyleOverridesChanged
   #============================================================================
   def onLayerStyleOverridesChanged(self):
      self.refreshOnMapCanvasExtent(self.layersToCheck, \
                                    self.checkPointLayer, self.checkLineLayer, self.checkPolygonLayer, \
                                    self.onlyEditableLayers)
      
      
   #============================================================================
   # getFeatures
   #============================================================================
   def getFeatures(self, layer, rect):
      layerId = layer.id()
      # verifica se layer esiste già nel dizionario
      if layerId in self.layerCacheAreaDict:
         return self.layerCacheAreaDict[layerId].getFeatures(rect)
      else:
         return []



################################
# funzioni generiche


#============================================================================
# getFeatureRequest
#============================================================================
def getFeatureRequest(rect, SubsetOfAttribute):
   request = QgsFeatureRequest()
   request.setFilterRect(rect)
   if SubsetOfAttribute == False:
      request.setSubsetOfAttributes([])
   return request


#===============================================================================
# getStrLayerGeomType
#===============================================================================
def getStrLayerGeomType(layer):
   wkbType = layer.wkbType()
   # WKBPointM = 2001, WKBPointZM = 3001
   if wkbType == QgsWkbTypes.Point or wkbType == QgsWkbTypes.PointZ or wkbType == 2001 or wkbType == 3001:
      return "Point"
   # WKBMultiPointM = 2004, WKBMultiPointZM = 3004
   elif wkbType == QgsWkbTypes.MultiPoint or wkbType == QgsWkbTypes.MultiPointZ or wkbType == 2004 or wkbType == 3004:
      return "MultiPoint"
   
   # WKBLineStringM = 2002, WKBLineStringZM = 3002
   elif wkbType == QgsWkbTypes.LineString or wkbType == QgsWkbTypes.LineStringZ or wkbType == 2002 or wkbType == 3002:
      return "LineString"
   # WKBMultiLineStringM = 2005, WKBMultiLineStringZM = 3005
   elif wkbType == QgsWkbTypes.MultiLineString or wkbType == QgsWkbTypes.MultiLineStringZ or wkbType == 2005 or wkbType == 3005:
      return "MultiLineString"
   
   # WKBPolygonM = 2003, WKBPolygonZM = 3003
   elif wkbType == QgsWkbTypes.Polygon or wkbType == QgsWkbTypes.PolygonZ or wkbType == 2003 or wkbType == 3003:
      return "Polygon"
   # WKBMultiPolygonM = 2006, WKBMultiPolygonZM = 3006
   elif wkbType == QgsWkbTypes.MultiPolygon or wkbType == QgsWkbTypes.MultiPolygonZ or wkbType == 2006 or wkbType == 3006:
      return "MultiPolygon"

   elif wkbType == QgsWkbTypes.NoGeometry:
      return "NoGeometry"

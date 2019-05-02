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
import math
import sys

from . import qad_utils
from .qad_variables import *
from .qad_msg import QadMsg


#===============================================================================
# QadEllipse ellipse class
#===============================================================================
class QadEllipse():
    
   def __init__(self, ellipse = None):
      if ellipse is not None:
         self.set(ellipse.center, ellipse.majorAxisFinalPt, ellipse.axisRatio, ellipse.startAngle, ellipse.endAngle)
      else:    
         self.center = None
         self.majorAxisFinalPt = None # punto finale dell'asse maggiore (a dx)
         self.axisRatio = 0 # rapporto tra asse minore e asse maggiore
         self.startAngle = 0.0 # l'ellisse può essere incompleta (come l'arco per il cerchio)
         self.endAngle = math.pi * 2 # A startAngle of 0 and endAngle of 2pi will produce a closed Ellipse.

   def whatIs(self):
      return "ELLIPSE"

   def set(self, center, majorAxisFinalPt, axisRatio, startAngle = 0.0, endAngle = math.pi * 2):
      if center == majorAxisFinalPt or radiusAxis > 1:
         return False
      self.center = QgsPointXY(center)
      self.majorAxisFinalPt = QgsPointXY(majorAxisFinalPt)
      self.axisRatio = axisRatio
      self.startAngle = startAngle
      self.endAngle = endAngle
      return True

   def transform(self, coordTransform):
      """Transform this geometry as described by CoordinateTranasform ct."""
      self.center = coordTransform.transform(self.center)      
      self.majorAxisFinalPt = coordTransform.transform(self.majorAxisFinalPt)      
   
   def transformFromCRSToCRS(self, sourceCRS, destCRS):
      """Transform this geometry as described by CRS."""
      if (sourceCRS is not None) and (destCRS is not None) and sourceCRS != destCRS:       
         coordTransform = QgsCoordinateTransform(sourceCRS, destCRS,QgsProject.instance()) # trasformo le coord
         self.center =  coordTransform.transform(self.center)
         self.majorAxisFinalPt =  coordTransform.transform(self.majorAxisFinalPt)
   
   def __eq__(self, ellipse):
      """self == other"""
      if self.center != ellipse.center or self.majorAxisFinalPt != ellipse.majorAxisFinalPt or self.axisRatio != ellipse.axisRatio or \
         self.majorAxisFinalPt != ellipse.startAngle or self.majorAxisFinalPt != ellipse.endAngle:
         return False
      else:
         return True    
  
   def __ne__(self, ellipse):
      """self != other"""
      if self.center != ellipse.center or self.majorAxisFinalPt != ellipse.majorAxisFinalPt or self.axisRatio != ellipse.axisRatio or \
         self.majorAxisFinalPt != ellipse.startAngle or self.majorAxisFinalPt != ellipse.endAngle:
         return True     
      else:
         return False             


   def length(self):
      if self.startAngle == 0 and self.endAngle == math.pi: # A startAngle of 0 and endAngle of 2pi will produce a closed Ellipse.
         a = qad_utils.getDistance(self.center, self.majorAxisFinalPt) # semiasse maggiore
         b = a * self.axisRatio # semiasse minore
         numerator = a * a + b * b
         if numerator == 0: return 0
         return 2 * math.pi * math.sqrt(numerator / 2)
      else:
         return 0 # da fare


   def area(self):
      if self.startAngle == 0 and self.endAngle == math.pi: # A startAngle of 0 and endAngle of 2pi will produce a closed Ellipse.
         a = qad_utils.getDistance(self.center, self.majorAxisFinalPt) # semiasse maggiore
         b = a * self.axisRatio # semiasse minore
         return  math.pi * a * b
      else:
         return 0 # da fare


   def getfocus(self):
      angle = qad_utils.getAngleBy2Pts(self.center, self.majorAxisFinalPt)
      a = qad_utils.getDistance(self.center, self.majorAxisFinalPt) # semiasse maggiore
      b = a * self.axisRatio # semiasse minore
      numerator = a * a + b * b
      if numerator == 0: return []
      c = math.sqrt(numerator)
      pt1 = qad_utils.getPolarPointByPtAngle(self.center, angle, c)
      pt2 = qad_utils.getPolarPointByPtAngle(self.center, angle, -c)
      return [pt1, pt2]
      
      
   def isPtOnEllipse(self, point):
      focus = self.getfocus()
      if len(focus) == 0: return False
      dist1 = qad_utils.getDistance(focus[0], self.majorAxisFinalPt)
      dist2 = qad_utils.getDistance(focus[1], self.majorAxisFinalPt)
      distSumEllipse = dist1 + dist2
      dist1 = qad_utils.getDistance(focus[0], point)
      dist2 = qad_utils.getDistance(focus[1], point)
      distSum = dist1 + dist2
      if qad_utils.doubleNear(distSumEllipse, distSum):
         if self.startAngle == 0 and self.endAngle == math.pi: # A startAngle of 0 and endAngle of 2pi will produce a closed Ellipse.
            return True
         else:
            angle = qad_utils.getAngleBy2Pts(self.center, point)
            return qad_utils.isAngleBetweenAngles(self.startAngle, self.endAngle, angle)
      return False


   def getQuadrantPoints(self):
      # ritorna i punti quadranti: pt in alto, pt in basso, a destra, a sinistra del centro
      angle = qad_utils.getAngleBy2Pts(self.center, self.majorAxisFinalPt)
      a = qad_utils.getDistance(self.center, self.majorAxisFinalPt) # semiasse maggiore
      b = a * self.axisRatio # semiasse minore

      pt1 = QgsPointXY(self.majorAxisFinalPt)
      pt2 = qad_utils.getPolarPointByPtAngle(self.center, angle + math.pi / 2, b)
      pt3 = qad_utils.getPolarPointByPtAngle(self.center, angle + math.pi, a)
      pt4 = qad_utils.getPolarPointByPtAngle(self.center, angle - math.pi / 2, b)

      if self.startAngle == 0 and self.endAngle == math.pi: # A startAngle of 0 and endAngle of 2pi will produce a closed Ellipse.
         return [pt1, pt2, pt3, pt4]
      else:
         res = []
         angle = qad_utils.getAngleBy2Pts(self.center, pt1)
         if qad_utils.isAngleBetweenAngles(self.startAngle, self.endAngle, angle): res.append(pt1)
         angle = qad_utils.getAngleBy2Pts(self.center, pt2)
         if qad_utils.isAngleBetweenAngles(self.startAngle, self.endAngle, angle): res.append(pt2)
         angle = qad_utils.getAngleBy2Pts(self.center, pt3)
         if qad_utils.isAngleBetweenAngles(self.startAngle, self.endAngle, angle): res.append(pt3)
         angle = qad_utils.getAngleBy2Pts(self.center, pt4)
         if qad_utils.isAngleBetweenAngles(self.startAngle, self.endAngle, angle): res.append(pt4)
         return res

         
   def getTanPoints(self, point):
      if self.startAngle == 0 and self.endAngle == math.pi: # A startAngle of 0 and endAngle of 2pi will produce a closed Ellipse.
         if self.isPtOnEllipse(point): return [point]
      else:
         closedEllipse = QadEllipse(self)
         closedEllipse.startAngle = 0.0
         closedEllipse.endAngle = math.pi * 2 # A startAngle of 0 and endAngle of 2pi will produce a closed Ellipse.
         if closedEllipse.isPtOnEllipse(point): return [point]
      
      return [] # da fare


   def getPerpendicularPoints(self, point):
      return [] # da fare


   def getIntersectionPointsWithEllipse(self, ellipse):
      return [] # da fare


   def getIntersectionPointsWithCircle(self, circle):
      return [] # da fare


   def getIntersectionPointsWithInfinityLine(self, p1, p2):
      return [] # da fare


   #============================================================================
   # getIntersectionPointsWithSegment
   #============================================================================
   def getIntersectionPointsWithSegment(self, p1, p2):
      return [] # da fare


   #============================================================================
   # getTangentsWithEllipse
   #============================================================================
   def getTangentsWithEllipse(self, ellipse):
      """
      la funzione ritorna una lista di linee che sono le tangenti alle due ellissi
      """
      return [] # da fare


   #============================================================================
   # getTangentsWithCircle
   #============================================================================
   def getTangentsWithCircle(self, circle):
      """
      la funzione ritorna una lista di linee che sono le tangenti tra ellisse e un cerchio
      """
      return [] # da fare
   
   
   #============================================================================
   # asPolyline
   #============================================================================
   def asPolyline(self, tolerance2ApproxCurve = None, atLeastNSegment = None):
      """
      ritorna una lista di punti che definisce la tangente
      """
      
      if tolerance2ApproxCurve is None:
         tolerance = QadVariables.get(QadMsg.translate("Environment variables", "TOLERANCE2APPROXCURVE"))
      else:
         tolerance = tolerance2ApproxCurve

      return [] # da fare
   
   
   #============================================================================
   # fromPolyline
   #============================================================================
   def fromPolylineXY(self, points, atLeastNSegment = None):
      """
      setta le caratteristiche dell'ellisse incontrata nella lista di punti.
      Ritorna True se é stato trovato un'ellissa altrimenti False.
      N.B. in punti NON devono essere in coordinate geografiche
      """
      totPoints = len(points)
   
      return False


   #============================================================================
   # rotate
   #============================================================================
   def rotate(self, basePt, angle):
      self.center = qad_utils.rotatePoint(self.center, basePt, angle)
      self.majorAxisFinalPt = qad_utils.rotatePoint(self.center, basePt, angle)


   #============================================================================
   # scale
   #============================================================================
   def scale(self, basePt, scale):
      self.majorAxisFinalPt = qad_utils.scalePoint(self.majorAxisFinalPt, self.center, scale)
      self.center = qad_utils.scalePoint(self.center, basePt, scale)


   #============================================================================
   # mirror
   #============================================================================
   def mirror(self, mirrorPt, mirrorAngle):
      self.center = qad_utils.mirrorPoint(self.center, mirrorPt, mirrorAngle)
      self.majorAxisFinalPt = qad_utils.mirrorPoint(self.center, mirrorPt, mirrorAngle)
      if self.startAngle != 0 or self.endAngle != math.pi: # ellisse aperta
         pass
      
      
   #============================================================================
   # fromFoci
   #============================================================================
   def fromFoci(self, f1, f2, ptOnEllipse, startAngle = 0.0, endAngle = math.pi * 2):
      """
      setta le caratteristiche dell'ellisse attraverso:
      i due fuochi
      un punto sull'ellisse
             /-ptOnEllipse-\
            /               \
            |   f1     f2   |
            \               /
             \-------------/
      """
      dist_f1f2 = qad_utils.getDistance(f1, f2)
      dist_f1PtOnEllipse = qad_utils.getDistance(f1, ptOnEllipse)
      dist_f2PtOnEllipse = qad_utils.getDistance(f2, ptOnEllipse)
      if dist_f1f2 == 0 or dist_f1PtOnEllipse == 0 or dist_f2PtOnEllipse == 0: return False

      dist_tot = dist_f1PtOnEllipse + dist_f2PtOnEllipse
      angle = qad_utils.getAngleBy2Pts(f1, f2)
      ptCenter = qad_utils.getMiddlePoint(f1, f2)
      
      majorAxisLen = dist_tot / 2.0 # semiasse maggiore
      minorAxisLen = math.sqrt((dist_tot/2.0)**2.0 - (dist_f1f2/2.0)**2.0) # semiasse minore
      axisRatio = minorAxisLen / majorAxisLen
      majorAxisPt = qad_utils.getPolarPointByPtAngle(ptCenter, angle, majorAxisLen)

      return self.set(ptCenter, majorAxisPt, axisRatio, startAngle, endAngle)
   

   #============================================================================
   # fromExtent
   #============================================================================
   def fromExtent(self, pt1, pt2, rot = 0, startAngle = 0.0, endAngle = math.pi * 2):
      """
      setta le caratteristiche dell'ellisse attraverso:
      i due di estensione (angoli opposti) del rettangolo che racchiude l'ellisse
      rotazione del rettangolo di estensione
             /-------------\  pt2
            /               \
            |               |
            \               /
        pt1  \-------------/
      """
      ptCenter = qad_utils.getMiddlePoint(pt1, pt2)
      halfDist = qad_utils.getDistance(pt1, pt2) / 2
      if halfDist == 0: return False
      angle = qad_utils.getAngleBy2Pts(pt1, pt2)
      angle = angle - rot
      projPt1 = qad_utils.getPolarPointByPtAngle(pt1, angle, halfDist)
      projPt2 = qad_utils.getPolarPointByPtAngle(pt1, angle, halfDist)

      majorAxisLen = abs(projPt1.x() - projPt2.x()) / 2.0 # semiasse maggiore
      minorAxisLen = abs(projPt1.y() - projPt2.y()) / 2.0 # semiasse minore
      axisRatio = minorAxisLen / majorAxisLen
      majorAxisPt = qad_utils.getPolarPointByPtAngle(ptCenter, rot, majorAxisLen)

      return self.set(ptCenter, majorAxisPt, axisRatio, startAngle, endAngle)


   #============================================================================
   # fromCenterAxis1FinalPtAxis2FinalPt
   #============================================================================
   def fromCenterAxis1FinalPtAxis2FinalPt(self, ptCenter, axis1FinalPt, axis2FinalPt, startAngle = 0.0, endAngle = math.pi * 2):
      """
      setta le caratteristiche dell'ellisse attraverso:
      il punto centrale
      il punto finale dell'asse
      il punto finale dell'altro asse
             /--axis2FinalPt--\
            /                  \
            |     ptCenter axis1FinalPt
            \                  /
             \----------------/
      """
      distAxis2 = qad_utils.getDistance(ptCenter, axis2FinalPt)
      return fromCenterAxis1FinalPtDistAxis2(cls, ptCenter, axis1FinalPt, distAxis2, startAngle, endAngle)


   #============================================================================
   # fromCenterAxis1FinalPtDistAxis2
   #============================================================================
   def fromCenterAxis1FinalPtDistAxis2(self, ptCenter, axis1FinalPt, distAxis2, startAngle = 0.0, endAngle = math.pi * 2):
      """
      setta le caratteristiche dell'ellisse attraverso:
      il punto centrale
      il punto finale dell'asse
      distanza dal centro al punto finale dell'altro asse
             /-------|--------\
            /     distAxis2    \
            |     ptCenter axis1FinalPt
            \                  /
             \----------------/
      """
      axis1Len = qad_utils.getDistance(ptCenter, axis1FinalPt)
      if axis1Len == 0 or distAxis2 == 0: return False
      axisRatio = axis1Len / distAxis2
      return self.set(ptCenter, axis1FinalPt, axisRatio, startAngle, endAngle)


   #============================================================================
   # fromCenterAxis1FinalPtAxis2FinalPt
   #============================================================================
   def fromCenterAxis1FinalPtAxis2FinalPt(self, axis1Finalpt1, axis1Finalpt2, axis2FinalPt, startAngle = 0.0, endAngle = math.pi * 2):
      """
      setta le caratteristiche dell'ellisse attraverso:
      il punto centrale
      il punto finale dell'asse
      il punto finale dell'altro asse
             /--axis2FinalPt--\
            /                  \
      axis1Finalpt2       axis1Finalpt1
            \                  /
             \----------------/
      """
      ptCenter = qad_utils.getMiddlePoint(xis1FinalPt1, axis1FinalPt2)
      axis2Len = qad_utils.getDistance(ptCenter, axis2FinalPt)
      return self.fromCenterAxis1FinalPtDistAxis2(ptCenter, axis1FinalPt, axis2Len, startAngle, endAngle)


   #============================================================================
   # fromAxis1FinalPtsAxis2Len
   #============================================================================
   def fromAxis1FinalPtsAxis2Len(self, axis1FinalPt1, axis1FinalPt2, distAxis2, startAngle = 0.0, endAngle = math.pi * 2):
      """
      setta le caratteristiche dell'ellisse attraverso:
      i punti finali dell'asse
      distanza dal centro al punto finale dell'altro asse
             /------|-------\
            /   distAxis2     \
         axis1pt2   |    axis1pt1
            \                /
             \--------------/
      """
      if distAxis2 == 0: return False
      ptCenter = qad_utils.getMiddlePoint(axis1FinalPt1, axis1FinalPt2)
      dist = qad_utils.getDistance(axis1FinalPt1, axis1FinalPt2)
      if dist == 0: return False
      axisRatio = distAxis2 / dist
      return self.set(ptCenter, axis1FinalPt1, axisRatio, startAngle, endAngle)

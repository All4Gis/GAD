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


# Classe che gestisce il comando UNDO
class QadUNDOCommandClass(QadCommandClass):

   def instantiateNewCmd(self):
      """ istanzia un nuovo comando dello stesso tipo """
      return QadUNDOCommandClass(self.plugIn)

   def getName(self):
      return QadMsg.translate("Command_list", "UNDO")

   def getEnglishName(self):
      return "UNDO"

   def connectQAction(self, action):
      action.triggered.connect(self.plugIn.runUNDOCommand)

   def getIcon(self):
      return QIcon(":/plugins/qad/icons/undo.svg")
   
   def getNote(self):
      # impostare le note esplicative del comando      
      return QadMsg.translate("Command_UNDO", "Reverses the effect of commands.")
   
   def __init__(self, plugIn):
      QadCommandClass.__init__(self, plugIn)
         
   def run(self, msgMapTool = False, msg = None):
      self.isValidPreviousInput = True # per gestire il comando anche in macro

      if self.step == 0: # inizio del comando
         keyWords = QadMsg.translate("Command_UNDO", "BEgin") + "/" + \
                    QadMsg.translate("Command_UNDO", "End") + "/" + \
                    QadMsg.translate("Command_UNDO", "Mark") + "/" + \
                    QadMsg.translate("Command_UNDO", "Back")
         default = 1
         prompt = QadMsg.translate("Command_UNDO", "Enter the number of operations to undo or [{0}] <{1}>: ").format(keyWords, str(default))
         
         englishKeyWords = "BEgin" + "/" + "End" + "/" + "Mark" + "/" + "Back"
         keyWords += "_" + englishKeyWords
         # si appresta ad attendere un numero intero positivo o enter o una parola chiave         
         # msg, inputType, default, keyWords, valori positivi
         self.waitFor(prompt, \
                      QadInputTypeEnum.INT | QadInputTypeEnum.KEYWORDS, \
                      default, \
                      keyWords, QadInputModeEnum.NOT_ZERO | QadInputModeEnum.NOT_NEGATIVE)      
         self.step = 1
         return False
   
      #=========================================================================
      # RISPOSTA ALLA RICHIESTA NUMERO INTERO (da step = 0)
      elif self.step == 1: # dopo aver atteso un punto o un numero reale si riavvia il comando
         if msgMapTool == True: # il punto arriva da una selezione grafica
            # la condizione seguente si verifica se durante la selezione di un punto
            # é stato attivato un altro plugin che ha disattivato Qad
            # quindi stato riattivato il comando che torna qui senza che il maptool
            # abbia selezionato un punto            
            if self.getPointMapTool().point is None: # il maptool é stato attivato senza un punto
               if self.getPointMapTool().rightButton == True: # se usato il tasto destro del mouse
                  self.plugIn.undoEditCommand()
                  return True # fine comando
               else:
                  self.setMapTool(self.getPointMapTool()) # riattivo il maptool
                  return False

            value = self.getPointMapTool().point
         else: # il punto arriva come parametro della funzione
            value = msg

         if type(value) == unicode:
            if value == QadMsg.translate("Command_UNDO", "BEgin") or value == "BEgin":
               self.plugIn.insertBeginGroup()
            elif value == QadMsg.translate("Command_UNDO", "End") or value == "End":
               if self.plugIn.insertEndGroup() == False:
                  self.showMsg(QadMsg.translate("Command_UNDO", "\nNo open group."))
            elif value == QadMsg.translate("Command_UNDO", "Mark") or value == "Mark":
               if self.plugIn.insertBookmark() == False:
                  self.showMsg(QadMsg.translate("Command_UNDO", "\nA mark can't be inserted into a group."))
            elif value == QadMsg.translate("Command_UNDO", "Back") or value == "Back":
               if self.plugIn.getPrevBookmarkPos() == -1: # non ci sono bookmark precedenti
                  keyWords = QadMsg.translate("QAD", "Yes") + "/" + \
                             QadMsg.translate("QAD", "No")
                  default = QadMsg.translate("QAD", "Yes")
                  prompt = QadMsg.translate("Command_UNDO", "This will undo everything. OK ? <{0}>: ").format(default)
                  
                  englishKeyWords = "Yes" + "/" + "No"
                  keyWords += "_" + englishKeyWords
                  # si appresta ad attendere enter o una parola chiave         
                  # msg, inputType, default, keyWords, nessun controllo
                  self.waitFor(prompt, \
                               QadInputTypeEnum.KEYWORDS, \
                               default, \
                               keyWords, QadInputModeEnum.NONE)
                  self.step = 2
                  return False                                       
               else:
                  self.plugIn.undoUntilBookmark()
         elif type(value) == int:
            self.plugIn.undoEditCommand(value)

         return True
         
      #=========================================================================
      # RISPOSTA ALLA RICHIESTA DI ANNULLARE TUTTO (da step = 1)
      elif self.step == 2: # dopo aver atteso una parola chiave si riavvia il comando
         if msgMapTool == True: # il punto arriva da una selezione grafica
            # la condizione seguente si verifica se durante la selezione di un punto
            # é stato attivato un altro plugin che ha disattivato Qad
            # quindi stato riattivato il comando che torna qui senza che il maptool
            # abbia selezionato un punto            
            if self.getPointMapTool().point is None: # il maptool é stato attivato senza un punto
               if self.getPointMapTool().rightButton == True: # se usato il tasto destro del mouse
                  self.plugIn.undoUntilBookmark()
                  self.showMsg(QadMsg.translate("Command_UNDO", "All has been undone."))
                  return True # fine comando
               else:
                  self.setMapTool(self.getPointMapTool()) # riattivo il maptool
                  return False

            value = self.getPointMapTool().point
         else: # il punto arriva come parametro della funzione
            value = msg

         if type(value) == unicode:
            if value == QadMsg.translate("QAD", "Yes") or value == "Yes":
               self.showMsg(QadMsg.translate("Command_UNDO", "All has been undone."))
               self.plugIn.undoUntilBookmark()

         return True # fine comando

   
# Classe che gestisce il comando REDO
class QadREDOCommandClass(QadCommandClass):
   
   def instantiateNewCmd(self):
      """ istanzia un nuovo comando dello stesso tipo """
      return QadREDOCommandClass(self.plugIn)

   def getName(self):
      return QadMsg.translate("Command_list", "REDO")

   def getEnglishName(self):
      return "REDO"

   def connectQAction(self, action):
      action.triggered.connect(self.plugIn.runREDOCommand)

   def getIcon(self):
      return QIcon(":/plugins/qad/icons/redo.svg")
   
   def getNote(self):
      # impostare le note esplicative del comando      
      return QadMsg.translate("Command_UNDO", "Reverses the effects of previous UNDO.")
   
   def __init__(self, plugIn):
      QadCommandClass.__init__(self, plugIn)
         
   def run(self, msgMapTool = False, msg = None):
      self.plugIn.redoEditCommand()
      return True   
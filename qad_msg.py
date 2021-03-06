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
from PyQt5.QtGui import * # for QDesktopServices
import os.path

import urllib
import platform
import sys

# traduction class.
class QadMsgClass():


   def __init__(self):
      pass
      

   #============================================================================
   # translate
   #============================================================================
   def translate(self, context, sourceText, disambiguation = None, n = -1):
      # da usare in una riga senza accoppiarla ad altre chiamate ad esempio (per lupdate.exe che altrimenti non le trova):
      # NON VA BENE
      #     proplist["blockScale"] = [QadMsg.translate("Dimension", "Scala frecce"), \
      #                               self.blockScale]
      # VA BENE
      #     msg = QadMsg.translate("Dimension", "Scala frecce")
      #     proplist["blockScale"] = [msg, self.blockScale]
 
      # contesti:
      # "QAD" per traduzioni generali
      # "Popup_menu_graph_window" per il menu popup nella finestra grafica
      # "Text_window" per la finestra testuale
      # "Command_list" per nomi di comandi
      # "Command_<nome comando in inglese>" per traduzioni di un comando specifico (es. "Command_PLINE")
      # "Snap" per i tipi di snap
      # finestre varie (es. "DSettings_Dialog", DimStyle_Dialog, ...)
      # "Dimension" per le quotature
      # "Environment variables" per i nomi delle variabili di ambiente
      # "Help" per i titoli dei capitoli del manuale che servono da section nel file html di help
      return QCoreApplication.translate(context, sourceText, disambiguation, n)


#===============================================================================
# qadShowPluginHelp
#===============================================================================
def qadShowPluginHelp(section = "", filename = "index", packageName = None):
   """
   show a help in the user's html browser.
   per conoscere la sezione/pagina del file html usare internet explorer,
   selezionare nella finestra di destra la voce di interesse e leggerne l'indirizzo dalla casella in alto.
   Questo perché internet explorer inserisce tutti i caratteri di spaziatura e tab che gli altri browser non fanno.
   """   
   try:
      source = ""
      if packageName is None:
         import inspect
         source = inspect.currentframe().f_back.f_code.co_filename
      else:
         source = sys.modules[packageName].__file__
   except:
      return

   # initialize locale
   userLocaleList = QSettings().value("locale/userLocale").split("_")
   language = userLocaleList[0]
   region = userLocaleList[1] if len(userLocaleList) > 1 else ""

   path = QDir.cleanPath(os.path.dirname(source) + "/help/help")
   helpPath = path + "_" + language + "_" + region # provo a caricare la lingua e la regione selezionate
   
   if not os.path.exists(helpPath):
      helpPath = path + "_" + language # provo a caricare la lingua
      if not os.path.exists(helpPath):
         helpPath = path + "_en" # provo a caricare la lingua inglese
         if not os.path.exists(helpPath):
            return
      
   helpfile = os.path.join(helpPath, filename + ".html")
   if os.path.exists(helpfile):
      url = "file:///"+helpfile

      if section != "":
         url = url + "#" + urllib.quote(section.encode('utf-8'))

      # la funzione QDesktopServices.openUrl in windows non apre la sezione
      if platform.system() == "Windows":
         import subprocess
         from winreg import HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, OpenKey, QueryValue
         # In Py3, this module is called winreg without the underscore
         
         try: # provo a livello di utente
            with OpenKey(HKEY_CURRENT_USER, r"Software\Classes\http\shell\open\command") as key:
               cmd = QueryValue(key, None)
         except: # se non c'era a livello di utente provo a livello di macchina
            with OpenKey(HKEY_LOCAL_MACHINE, r"Software\Classes\http\shell\open\command") as key:
               cmd = QueryValue(key, None)
   
         if cmd.find("\"%1\"") >= 0:
            subprocess.Popen(cmd.replace("%1", url))
         else:    
            if cmd.find("%1") >= 0:
               subprocess.Popen(cmd.replace("%1", "\"" + url + "\""))       
            else:
               subprocess.Popen(cmd + " \"" + url + "\"")
      else:
         QDesktopServices.openUrl(QUrl(url))           
   
   
#===============================================================================
# QadMsg = variabile globale
#===============================================================================

QadMsg = QadMsgClass()

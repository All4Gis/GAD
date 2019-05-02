# --------------------------------------------------------
#   GAD - Geographic Aided Design
#
#    begin      : April 26, 2019
#    copyright  : (c) 2019 by German Perez-Casanova Gomez
#    email      : german.perez-casanova@rte-france.com
#
# --------------------------------------------------------
#   GAD is free software and is offered without guarantee
#   or warranty. You can redistribute it and/or modify it
#   under the terms of version 2 of the GNU General Public
#   License (GPL v2) as published by the Free Software
#   Foundation (www.gnu.org).
# --------------------------------------------------------

def classFactory(iface):
    # load Qad class from file qad
    from .qad import Qad
    return Qad(iface)

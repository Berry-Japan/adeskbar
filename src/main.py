#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  ADesk Bar - Quick application launcher
#
#  by ADcomp <david.madbox@gmail.com>
#  http://www.ad-comp.be/
#
#  This program is distributed under the terms of the GNU General Public License
#  For more info see http://www.gnu.org/licenses/gpl.txt
##

import os
import sys

if __name__ == "__main__":
    
    realpath = os.path.dirname(os.path.realpath( __file__ ))
    os.chdir(realpath)
    
    if len(sys.argv) == 2:
        cfg_file = sys.argv[1]
    else:
        cfg_file = 'default'
        
    if cfg_file == '--check':
        import adesk.check
        adesk.check.run()
    else:
        import adesk.bar
        bar_manager = adesk.bar.BarManager(cfg_file)
        bar_manager.run()

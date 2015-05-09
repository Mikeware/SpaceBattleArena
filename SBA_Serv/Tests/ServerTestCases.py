"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from TestCaseRigging import SBAServerTestCase
import Server.MWNL2 as MWNL2

import time

class ServerConnectTestCase(SBAServerTestCase):

    def test_make_connection(self):
        net = MWNL2.MWNL_Init(self.cfg.getint("Server", "port"), self.callback)
        net.connect("localhost")

        x = 0
        while not net.haveID() and not net.iserror() and x < 5:
            x += 1
            time.sleep(1)

        self.assertEqual(net.iserror(), False, "Network Error on Connect")
        self.assertEqual(net.isconnected(), True, "Didn't Connect to Server")
        self.assertEqual(net.haveID(), True, "Don't have Server ID")
        
        net.close()

        x = 0
        while net.haveID() and not net.iserror() and x < 5:
            x += 1
            time.sleep(1)

        self.assertEqual(net.isconnected(), False, "Didn't Disconnect from Server")

    def callback(self, sender, cmd):
        pass

if __name__ == '__main__':
    unittest.main()

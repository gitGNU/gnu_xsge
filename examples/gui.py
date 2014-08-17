#!/usr/bin/env python3

# Multiple Rooms Example
# Written in 2014 by Julian Marchant <onpon4@riseup.net>
#
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sge
from xsge import gui


class Game(sge.Game):

    def event_game_start(self):
        sge.keyboard.set_repeat(interval=10, delay=500)

    def event_close(self):
        self.end()


class Room(sge.Room):

    def event_room_start(self):
        self.handler = gui.Handler.create()

        window = gui.Window(self.handler, 8, 8, 240, 240, title="Test window 1")
        button = gui.Button(window, 8, 8, 0, "My button")
        gui.Label(window, 8, 32, 0, "My label")
        gui.Label(window, 8, 64, 0, "my label " * 50, width=224)
        button2 = gui.Button(window, 16, 100, 5, "Another button", width=150)

        def event_press(handler=self.handler):
            gui.show_message("You just pressed my buttons!", parent=handler)

        button.event_press = event_press

        def event_press(handler=self.handler):
            name = gui.get_text_entry("Who are you?!", parent=handler)
            if name:
                m = "{}? That's a suspicious name!".format(name)
            else:
                m = "Won't talk, eh? I've got my eye on you!"

            gui.show_message(m, parent=handler)

        button2.event_press = event_press

        window.show()

        window2 = gui.Window(self.handler, 480, 200, 320, 320,
                             title="Test window 2")
        gui.CheckBox(window2, 16, 16, 0)
        gui.RadioButton(window2, 16, 48, 0)
        gui.RadioButton(window2, 16, 80, 0)
        gui.RadioButton(window2, 16, 112, 0)
        gui.ProgressBar(window2, 16, 144, 0, 288, progress=0.5)
        gui.TextBox(window2, 16, 176, 0, width=288, text="mytext")
        window2.show()


def main():
    Game(width=800, height=600)
    gui.init()

    Room()

    sge.game.start()


if __name__ == '__main__':
    main()

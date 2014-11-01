#!/usr/bin/env python3

# Transitions example
# Written in 2012, 2013, 2014 by Julian Marchant <onpon4@riseup.net>
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

import random

import sge
from xsge import transition


class glob(object):

    font = None
    pop_sound = None
    music = None


class Game(sge.Game):

    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


class Circle(sge.Object):

    def __init__(self, x, y):
        super(Circle, self).__init__(x, y, 5, sprite='circle',
                                     collision_precise=True)

    def event_create(self):
        self.image_alpha = 200
        if self.collision(sge.game.mouse):
            self.image_blend = sge.Color('#ff0000')
        else:
            self.image_blend = sge.Color('blue')

    def event_mouse_move(self, x, y):
        if self.collision(sge.game.mouse):
            self.image_blend = sge.Color("red")
        else:
            self.image_blend = sge.Color((0, 0, 255))

    def event_mouse_button_press(self, button):
        if button == 'left':
            if self.collision(sge.game.mouse):
                self.destroy()

    def event_destroy(self):
        pop = CirclePop(self.x, self.y)
        pop.image_blend = self.image_blend
        sge.game.current_room.add(pop)
        assert glob.pop_sound is not None
        glob.pop_sound.play()


class CirclePop(sge.Object):

    def __init__(self, x, y):
        super(CirclePop, self).__init__(x, y, 5, sprite='circle_pop',
                                        tangible=False)

    def event_animation_end(self):
        self.destroy()

    def event_destroy(self):
        circle = Circle(random.randint(0, sge.game.width),
                        random.randint(0, sge.game.height))
        sge.game.current_room.add(circle)


class Room(transition.Room):

    def __init__(self, text, objects=(), views=None, background=None):
        self.text = text
        super(Room, self).__init__(objects, views=views, background=background)

    def event_room_start(self):
        super(Room, self).event_room_start()
        self.event_room_resume()

    def event_room_resume(self):
        glob.music.play(loops=None)

    def event_key_press(self, key, char):
        if key == "1":
            self.transition_end(transition=transition.FADE)
        elif key == "2":
            self.transition_end(transition=transition.DISSOLVE)
        elif key == "3":
            self.transition_end(transition=transition.PIXELATE)
        elif key == "4":
            self.transition_end(transition=transition.WIPE_LEFT)
        elif key == "5":
            self.transition_end(transition=transition.WIPE_RIGHT)
        elif key == "6":
            self.transition_end(transition=transition.WIPE_TOP)
        elif key == "7":
            self.transition_end(transition=transition.WIPE_BOTTOM)
        elif key == "8":
            self.transition_end(transition=transition.WIPE_TOPLEFT)
        elif key == "9":
            self.transition_end(transition=transition.WIPE_TOPRIGHT)
        elif key == "0":
            self.transition_end(transition=transition.WIPE_BOTTOMLEFT)
        elif key == "q":
            self.transition_end(transition=transition.WIPE_BOTTOMRIGHT)
        elif key == "w":
            self.transition_end(transition=transition.WIPE_MATRIX)
        elif key == "e":
            self.transition_end(transition=transition.IRIS_IN)
        elif key == "r":
            self.transition_end(transition=transition.IRIS_OUT)


def main():
    # Create Game object
    game = Game(collision_events_enabled=False)

    # Load sprites
    circle_sprite = sge.Sprite('circle', width=64, height=64, origin_x=32,
                               origin_y=32)
    circle_pop_sprite = sge.Sprite('circle_pop', width=64, height=64,
                                   origin_x=32, origin_y=32, fps=60)
    fence_sprite = sge.Sprite('fence')

    # Load backgrounds
    layers = [sge.BackgroundLayer(fence_sprite, 0, 380, 0, yrepeat=False)]
    layers2 = [sge.BackgroundLayer(fence_sprite, 0, 0, 0)]
    background = sge.Background(layers, sge.Color(0xffffff))
    background2 = sge.Background(layers2, sge.Color('white'))

    # Load fonts
    glob.font = sge.Font('Liberation Serif', 20)

    # Load sounds
    glob.pop_sound = sge.Sound('pop.ogg')
    
    # Load music
    glob.music = sge.Music('WhereWasI.ogg')

    # Create objects
    circle = Circle(game.width // 2, game.height // 2)
    circle2 = Circle(22, 48)
    circle3 = Circle(486, 301)
    circle4 = Circle(50, 400)
    circle5 = Circle(game.width // 2, game.height // 2)
    circle6 = Circle(52, 120)
    objects = [circle, circle2, circle3, circle4]
    objects2 = [circle5, circle6]

    # Create view
    views = [sge.View(0, 0)]

    # Create rooms
    room1 = Room('I am the first room!', objects, views=views, background=background)
    room2 = Room('Second room on the house!', objects2, background=background2)
    room3 = Room('I am the third room!', objects, views=views, background=background)
    room4 = Room('Fourth room on the house!', objects2, background=background2)
    room5 = Room('I am the fifth room!', objects, views=views, background=background)
    room6 = Room('Sixth room on the house!', objects2, background=background2)

    game.start()


if __name__ == '__main__':
    main()

# xSGE Transition Framework
# Copyright (C) 2014 Julian Marchant <onpon4@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This module provides a framework for transition animations.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import math
import random

import sge
import six


__all__ = ["Room"]

FADE = 1
DISSOLVE = 2
PIXELATE = 3
WIPE_LEFT = 4
WIPE_RIGHT = 5
WIPE_TOP = 6
WIPE_BOTTOM = 7
WIPE_TOPLEFT = 8
WIPE_TOPRIGHT = 9
WIPE_BOTTOMLEFT = 10
WIPE_BOTTOMRIGHT = 11
WIPE_MATRIX = 12
IRIS_IN = 13
IRIS_OUT = 14


class Room(sge.Room):

    """
    This class is a variant of :class:`sge.Room` with transition
    support.  Transitions are done using
    :meth:`xsge.transition.Room.show_transition`.  In general, it is
    best to use :meth:`xsge.transition.Room.transition_start`,
    :meth:`xsge.transition.Room.transition_resume`, and
    :meth:`xsge.transition.Room.transition_end`, which show transitions
    in between the current and next room.
    """

    transition_update = None
    transition_sprite = None
    transition_duration = 0

    def event_room_start(self):
        self.transition_time_passed = 0
        self.transition_complete_last = 0
        self.transition_variables = {}

    def _update_fade(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height
        if complete < 0.5:
            diff = (complete - self.transition_complete_last) * 2
            c = sge.Color([int(round(diff * 255))] * 3)
            darkener = sge.Sprite(width=self.transition_sprite.width,
                                  height=self.transition_sprite.height)
            darkener.draw_rectangle(0, 0, w, h, c)
            self.transition_sprite.draw_sprite(
                darkener, 0, 0, 0, blend_mode=sge.BLEND_RGB_SUBTRACT)
            darkener.destroy()
        else:
            complete = (complete - 0.5) * 2
            c = sge.Color((0, 0, 0, int(round(255 - complete * 255))))
            self.transition_sprite.draw_clear()
            self.transition_sprite.draw_rectangle(0, 0, w, h, fill=c)

    def _update_dissolve(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height
        diff = complete - self.transition_complete_last
        c = sge.Color((0, 0, 0, int(round(diff * 255))))
        eraser = sge.Sprite(width=self.transition_sprite.width,
                            height=self.transition_sprite.height)
        eraser.draw_rectangle(0, 0, w, h, c)
        self.transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                           blend_mode=sge.BLEND_RGBA_SUBTRACT)
        eraser.destroy()

    def _update_pixelate(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height
        if complete < 0.5:
            complete *= 2
            swidth = max(1, w * (1 - complete))
            sheight = max(1, h * (1 - complete))
            self.transition_sprite.width = swidth
            self.transition_sprite.height = sheight
            self.transition_sprite.width = w
            self.transition_sprite.height = h
        else:
            diff = (complete - self.transition_complete_last) * 2
            c = sge.Color((0, 0, 0, int(round(diff * 255))))
            eraser = sge.Sprite(width=self.transition_sprite.width,
                                height=self.transition_sprite.height)
            eraser.draw_rectangle(0, 0, w, h, c)
            self.transition_sprite.draw_sprite(
                eraser, 0, 0, 0, blend_mode=sge.BLEND_RGBA_SUBTRACT)
            eraser.destroy()

    def _update_wipe_left(self, complete):
        w = self.transition_sprite.width * complete
        h = self.transition_sprite.height
        self.transition_sprite.draw_erase(0, 0, w, h)

    def _update_wipe_right(self, complete):
        w = self.transition_sprite.width * complete
        x = self.transition_sprite.width - w
        h = self.transition_sprite.height
        self.transition_sprite.draw_erase(x, 0, w, h)

    def _update_wipe_top(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height * complete
        self.transition_sprite.draw_erase(0, 0, w, h)

    def _update_wipe_bottom(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height * complete
        y = self.transition_sprite.height - h
        self.transition_sprite.draw_erase(0, y, w, h)

    def _update_wipe_topleft(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height
        x = w * complete * 2
        y = h * complete * 2
        eraser = sge.Sprite(width=w, height=h)
        eraser.draw_polygon([(0, 0), (x, 0), (0, y)],
                            fill=sge.Color((0, 0, 0, 255)), anti_alias=True)
        self.transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                           blend_mode=sge.BLEND_RGBA_SUBTRACT)
        eraser.destroy()

    def _update_wipe_topright(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height
        x = w - w * complete * 2
        y = h * complete * 2
        eraser = sge.Sprite(width=w, height=h)
        eraser.draw_polygon([(w, 0), (x, 0), (w, y)],
                            fill=sge.Color((0, 0, 0, 255)), anti_alias=True)
        self.transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                           blend_mode=sge.BLEND_RGBA_SUBTRACT)
        eraser.destroy()

    def _update_wipe_bottomleft(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height
        x = w * complete * 2
        y = h - h * complete * 2
        eraser = sge.Sprite(width=w, height=h)
        eraser.draw_polygon([(0, h), (x, h), (0, y)],
                            fill=sge.Color((0, 0, 0, 255)), anti_alias=True)
        self.transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                           blend_mode=sge.BLEND_RGBA_SUBTRACT)
        eraser.destroy()

    def _update_wipe_bottomright(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height
        x = w - w * complete * 2
        y = h - h * complete * 2
        eraser = sge.Sprite(width=w, height=h)
        eraser.draw_polygon([(w, h), (x, h), (w, y)],
                            fill=sge.Color((0, 0, 0, 255)), anti_alias=True)
        self.transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                           blend_mode=sge.BLEND_RGBA_SUBTRACT)
        eraser.destroy()
        

    def _update_wipe_matrix(self, complete):
        psize = 4
        w = self.transition_sprite.width
        h = self.transition_sprite.height
        mw = int(round(w / psize))
        mh = int(round(h / psize))
        if "remaining" in self.transition_variables:
            remaining = self.transition_variables["remaining"]
        else:
            remaining = []
            for x in six.moves.range(mw):
                for y in six.moves.range(mh):
                    remaining.append((x, y))

        diff = complete - self.transition_complete_last
        new_erase = int(round(mw * mh * diff))
        self.transition_sprite.draw_lock()
        while new_erase > 0 and remaining:
            new_erase -= 1
            x, y = remaining.pop(random.randrange(len(remaining)))
            self.transition_sprite.draw_erase(x * psize, y * psize, psize,
                                              psize)
        self.transition_sprite.draw_unlock()

        self.transition_variables["remaining"] = remaining

    def _update_iris_in(self, complete):
        x = self.transition_sprite.width / 2
        y = self.transition_sprite.height / 2
        r = int(round(math.hypot(x, y) * (1 - complete)))
        eraser = sge.Sprite(width=self.transition_sprite.width,
                            height=self.transition_sprite.height)
        eraser_eraser = sge.Sprite(width=self.transition_sprite.width,
                                   height=self.transition_sprite.height)
        eraser_eraser.draw_circle(x, y, r, fill=sge.Color((0, 0, 0, 255)))

        eraser.draw_lock()
        eraser.draw_rectangle(0, 0, eraser.width, eraser.height,
                              fill=sge.Color((0, 0, 0, 255)))
        eraser.draw_sprite(eraser_eraser, 0, 0, 0,
                           blend_mode=sge.BLEND_RGBA_SUBTRACT)
        eraser.draw_unlock()
        eraser_eraser.destroy()

        self.transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                           blend_mode=sge.BLEND_RGBA_SUBTRACT)
        eraser.destroy()

    def _update_iris_out(self, complete):
        x = self.transition_sprite.width / 2
        y = self.transition_sprite.height / 2
        r = int(round(math.hypot(x, y) * complete))
        eraser = sge.Sprite(width=self.transition_sprite.width,
                            height=self.transition_sprite.height)
        eraser.draw_circle(x, y, r, fill=sge.Color((0, 0, 0, 255)))
        self.transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                           blend_mode=sge.BLEND_RGBA_SUBTRACT)
        eraser.destroy()

    def show_transition(self, transition, sprite, duration):
        """Show a transition.

        Arguments:

        - ``transition`` -- The type of transition to use.  Should be
          one of the following:

          - :const:`xsge.transition.FADE` -- Fade out (to black) and
            then fade in.

          - :const:`xsge.transition.DISSOLVE` -- Gradually replace the
            first room with the second room.

          - :const:`xsge.transition.PIXELATE` -- Pixelate the first
            room, then fade into the second room.  If
            :attr:`sge.game.scale_smooth` is :const:`True`, the effect
            will instead be to blur and unblur the rooms.  This relies
            on the destructiveness of changing :attr:`sge.Sprite.width`
            and :attr:`sge.Sprite.height`.

          - :const:`xsge.transition.WIPE_LEFT` -- Wipe transition from
            left to right.

          - :const:`xsge.transition.WIPE_RIGHT` -- Wipe transition from
            right to left.

          - :const:`xsge.transition.WIPE_TOP` -- Wipe transition from
            top to bottom.

          - :const:`xsge.transition.WIPE_BOTTOM` -- Wipe transition from
            bottom to top.

          - :const:`xsge.transition.WIPE_TOPLEFT` -- Diagonal wipe
            transition from top-left to bottom-right.

          - :const:`xsge.transition.WIPE_TOPRIGHT` -- Diagonal wipe
            transition from top-right to bottom-left.

          - :const:`xsge.transition.WIPE_BOTTOMLEFT` -- Diagonal wipe
            transition from bottom-left to top-right.

          - :const:`xsge.transition.WIPE_BOTTOMRIGHT` -- Diagonal wipe
            transition from bottom-right to top-left.

          - :const:`xsge.transition.WIPE_MATRIX` -- Matrix wipe
            transition.

          - :const:`xsge.transition.IRIS_IN` -- Iris in transition.

          - :const:`xsge.transition.IRIS_OUT` -- Iris out transition.

        - ``sprite`` -- The sprite to use as the first image (the one
          being transitioned out of).  Generally should be a screenshot
          of the previous room.

        - ``duration`` -- The time the transition should take in
          milliseconds.

        """
        self.transition_update = {
            FADE: self._update_fade, DISSOLVE: self._update_dissolve,
            PIXELATE: self._update_pixelate, WIPE_LEFT: self._update_wipe_left,
            WIPE_RIGHT: self._update_wipe_right,
            WIPE_TOP: self._update_wipe_top,
            WIPE_BOTTOM: self._update_wipe_bottom,
            WIPE_TOPLEFT: self._update_wipe_topleft,
            WIPE_TOPRIGHT: self._update_wipe_topright,
            WIPE_BOTTOMLEFT: self._update_wipe_bottomleft,
            WIPE_BOTTOMRIGHT: self._update_wipe_bottomright,
            WIPE_MATRIX: self._update_wipe_matrix,
            IRIS_IN: self._update_iris_in, IRIS_OUT: self._update_iris_out
            }.setdefault(transition, lambda c: None)
        self.transition_sprite = sprite
        self.transition_duration = duration
        self.transition_time_passed = 0
        self.transition_complete_last = 0
        self.transition_variables = {}

    def transition_start(self, transition=FADE, duration=1500):
        """Start the room, using a transition.

        See the documentation for :meth:`sge.Room.start` and
        :meth:`xsge.transition.Room.show_transition` for more
        information.

        """
        screenshot = sge.Sprite.from_screenshot()
        self.show_transition(transition, screenshot, duration)
        self.start()

    def transition_resume(self, transition=FADE, duration=1500):
        """Resume the room, using a transition.

        See the documentation for :meth:`sge.Room.resume` and
        :meth:`xsge.transition.Room.show_transition` for more
        information.

        """
        screenshot = sge.Sprite.from_screenshot()
        self.show_transition(transition, screenshot, duration)
        self.resume()

    def transition_end(self, transition=FADE, duration=1500, next_room=None,
                       resume=True):
        """End the room, using a transition for the next room.

        See the documentation for :meth:`sge.Room.end` and
        :meth:`xsge.transition.Room.show_transition` for more
        information.

        """
        if next_room is None:
            next_room = self.room_number + 1

        if (next_room >= -len(sge.game.rooms) and
                next_room < len(sge.game.rooms)):
            screenshot = sge.Sprite.from_screenshot()
            sge.game.rooms[next_room].show_transition(transition, screenshot,
                                                      duration)

        self.end(next_room=next_room, resume=resume)

    def event_step(self, time_passed, delta_mult):
        if (self.transition_update is not None and
                self.transition_sprite is not None and
                self.transition_duration > 0):
            self.transition_time_passed += time_passed

            if self.transition_time_passed < self.transition_duration:
                complete = (self.transition_time_passed /
                            self.transition_duration)
                self.transition_update(complete)
                self.transition_complete_last = complete
                sge.game.project_sprite(self.transition_sprite, 0, 0, 0)
            else:
                self.transition_sprite.destroy()
                self.transition_update = None
                self.transition_sprite = None
                self.transition_duration = 0
                self.transition_time_passed = 0
                self.transition_complete_last = 0
                self.transition_variables = {}

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.04.09 23:00:00                  #
# ================================================== #

import os

from .capture import Capture
from .common import Common


class Painter:
    def __init__(self, window=None):
        """
        Painter controller

        :param window: Window instance
        """
        self.window = window
        self.capture = Capture(window)
        self.common = Common(window)

    def setup(self):
        """Setup painter"""
        self.restore()
        size = "800x600"  # default size
        if self.window.core.config.has('painter.canvas.size'):
            size = self.window.core.config.get('painter.canvas.size')
        self.common.change_canvas_size(size)
        self.common.restore_brush_settings()

    def open(self, path: str):
        """
        Open image from file

        :param path: path to image
        """
        self.window.ui.painter.open_image(path)
        self.window.ui.status("Image loaded: " + os.path.basename(path))

    def open_external(self, path: str):
        """
        Open image from file (from external)

        :param path: path to image
        """
        self.open(path)
        if not self.is_active():
            self.window.controller.ui.switch_tab('draw')

    def save(self):
        """Store current image"""
        path = os.path.join(self.common.get_capture_dir(), '_current.png')
        self.window.ui.painter.image.save(path)

    def save_all(self):
        """Save all (on exit)"""
        self.save()

    def restore(self):
        """Restore previous image"""
        path = os.path.join(self.common.get_capture_dir(), '_current.png')
        if os.path.exists(path):
            self.window.ui.painter.image.load(path)
        else:
            # clear image
            self.window.ui.painter.clear_image()
        self.window.ui.painter.update()

    def is_active(self) -> bool:
        """
        Check if painter is enabled

        :return: True if painter is current active tab
        """
        return self.window.controller.ui.current_tab == self.window.controller.ui.tab_idx['draw']

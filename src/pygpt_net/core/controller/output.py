#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.02 14:00:00                  #
# ================================================== #

from datetime import datetime
from PySide6.QtGui import QTextCursor


class Output:
    def __init__(self, window=None):
        """
        Output controller

        :param window: main window
        """
        self.window = window

    def setup(self):
        """Setups output"""
        self.window.data['output.timestamp'].setChecked(self.window.config.data['output_timestamp'])

    def clear(self):
        """
        Clears output
        """
        self.window.data['output'].clear()

    def append_context(self):
        """
        Appends context to output
        """
        for item in self.window.gpt.context.items:
            self.append_context_item(item)

    def append_context_item(self, item):
        """
        Appends context item to output

        :param item: context item
        """
        self.append_input(item)
        self.append_output(item)

    def append_input(self, item):
        """
        Appends input to output

        :param item: context item
        """
        if item.input is None or item.input == "":
            return
        if self.window.config.data['output_timestamp'] and item.input_timestamp is not None:
            name = ""
            if item.input_name is not None and item.input_name != "":
                name = item.input_name + " "
            ts = datetime.fromtimestamp(item.input_timestamp)
            hour = ts.strftime("%H:%M:%S")
            self.append("{}{}: > {}".format(name, hour, item.input))
        else:
            self.append("> {}".format(item.input))

    def append_output(self, item):
        """
        Appends output to output

        :param item: context item
        """
        if item.output is None or item.output == "":
            return
        if self.window.config.data['output_timestamp'] and item.output_timestamp is not None:
            name = ""
            if item.output_name is not None and item.output_name != "":
                name = item.output_name + " "
            ts = datetime.fromtimestamp(item.output_timestamp)
            hour = ts.strftime("%H:%M:%S")
            self.append("{}{}: {}".format(name, hour, item.output) + "\n")
        else:
            self.append(item.output + "\n")

    def append_chunk(self, item, text_chunk, begin=False):
        """
        Appends output to output

        :param item: context item
        :param text_chunk: text chunk
        :param begin: if it is the beginning of the text

        """
        if text_chunk is None or text_chunk == "":
            return
        if begin and self.window.config.data['output_timestamp'] and item.output_timestamp is not None:
            name = ""
            if item.output_name is not None and item.output_name != "":
                name = item.output_name + " "
            ts = datetime.fromtimestamp(item.output_timestamp)
            hour = ts.strftime("%H:%M:%S")
            self.append("{}{}: ".format(name, hour), "")

        self.append(text_chunk, "")

    def append(self, text, end="\n"):
        """
        Appends text to output

        :param text: text to append
        :param end: end of the line
        """
        cur = self.window.data['output'].textCursor()  # Move cursor to end of text
        cur.movePosition(QTextCursor.End)
        s = str(text) + end
        while s:
            head, sep, s = s.partition("\n")  # Split line at LF
            cur.insertText(head)  # Insert text at cursor
            if sep:  # New line if LF
                cur.insertBlock()
        self.window.data['output'].setTextCursor(cur)  # Update visible cursor

    def toggle_timestamp(self, value):
        """
        Toggles timestamp

        :param value: value of the checkbox
        """
        self.window.config.data['output_timestamp'] = value
        self.window.config.save()
        self.window.controller.context.refresh()

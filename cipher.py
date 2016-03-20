#
# cipher.py
# Cipher, a deobfuscation tool for Sublime Text 3
#
# Written by Metin Carlo DePaolis
# Copyright (c) 2017 Metin Carlo DePaolis
#
# License: MIT
#

import base64

import sublime
import sublime_plugin


def remove_null_bytes(s):
    return s.replace('\x00', '')


class Cipher(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                region = sublime.Region(0, self.view.size())
            region_text = self.view.substr(region)
            transumted_region = self.transmute(region_text)
            self.view.replace(edit, region, transumted_region)


class Base64EncodeCommand(Cipher):
    def transmute(self, text):
        text = text.encode('raw_unicode_escape')
        return base64.b64encode(text).decode('ascii')


class Base64DecodeCommand(Cipher):
    def pad(self, text):
        mod = len(text) % 4
        if mod == 3:
            text = text + '='
        elif mod == 2:
            text = text + '=='
        elif mod == 1:
            text = text + '==='
        return text

    def transmute(self, text):
        b64 = base64.b64decode(self.pad(text)).decode('raw_unicode_escape')
        return b64

#
# cipher.py
# Cipher, a deobfuscation tool for Sublime Text 3
#
# Written by Metin Carlo DePaolis
# Copyright (c) 2016 Metin Carlo DePaolis
#
# License: MIT
#

import re
import sys
import base64
import urllib

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


class Base64EncodeCommand(Cipher):
    def transmute(self, text):
        text = text.encode('raw_unicode_escape')
        return base64.b64encode(text).decode('ascii')


class UrlDecode(Cipher):
    def transmute(self, text):
        try:
            result = urllib.parse.unquote(text)
        except:
            e = sys.exc_info()[1]
            result = str(e)
        return result


class UrlEncode(Cipher):
    def transmute(self, text):
        return urllib.parse.quote(text)


class UnicodeEscapeDecodeCommand(Cipher):
    def transmute(self, text):
        transmutation = (text.encode('ascii')).decode('unicode_escape')
        return transmutation


class UnicodeEscapeEncodeCommand(Cipher):
    def transmute(self, text):
        return "Not implemented... yet?"


class UnicodeAndUrlDecodeCommand(Cipher):
    def transmute(self, text):
        unicode_decoded = (text.encode('ascii')).decode('unicode_escape')
        transmutation = urllib.parse.unquote(unicode_decoded)
        return transmutation


class UnicodeAndUrlEncodeCommand(Cipher):
    def transmute(self, text):
        return "Not implemented... yet?"


class FromCharCodeArray(Cipher):
    def transmute(self, text):
        text = text.replace('[', '')
        text = text.replace(']', '')
        re.sub(r'\s+', '', text)        # remove all whitespace
        arr = text.split(',')
        arr = [int(i) for i in arr]
        transmutation = ''.join(map(chr, arr))
        return transmutation


class RemoveNulls(Cipher):
    def transmute(self, text):
        return remove_null_bytes(text)


class CombineStringConcatenation(Cipher):
    def transmute(self, text):
        transmutation = re.sub('"\s*\+\s*\"', '', text)
        return transmutation

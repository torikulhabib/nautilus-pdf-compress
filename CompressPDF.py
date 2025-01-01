#!/usr/bin/env python3

import os, subprocess

from urllib.parse import unquote, urlparse

import gi
from gi.repository import GObject, Nautilus



def uri_to_path(file):
    p = urlparse(file.get_activation_uri())
    return os.path.abspath(os.path.join(p.netloc, unquote(p.path)))


class CompressPDF(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        GObject.Object.__init__(self)

    def send_comp(self, menu, files):
        for file in files:
            subprocess.Popen(["/usr/bin/gs"] + ['-sDEVICE=pdfwrite'] + ['-dCompatibilityLevel=1.4'] + ['-dDownsampleColorImages=true'] + ['-dColorImageResolution=150'] + ['-dNOPAUSE'] + ['-dBATCH'] + ['-sOutputFile='+ os.path.dirname(uri_to_path(file)) + '/New-' + os.path.splitext(os.path.basename(uri_to_path(file)))[0] + '.pdf'] + ['-f'] + [uri_to_path(file)])

    def send_merge(self, menu, files, resolustion):
        paths = []
        for file in files:
            paths.append(uri_to_path(file))
        subprocess.Popen(["/usr/bin/gs"] + ['-sDEVICE=pdfwrite'] + ['-dCompatibilityLevel=1.4'] + ['-dDownsampleColorImages=true'] + ['-dColorImageResolution=' + resolustion] + ['-dNOPAUSE'] + ['-dBATCH'] + ['-sOutputFile='+ os.path.dirname(uri_to_path(file)) +'/Merged-' + resolustion+ '.pdf'] + ['-f'] + paths)

    def get_file_items(self, *args):
        files = args[-1]
        if len(files) < 1:
            return

        for file in files:
            if file.is_directory():
                return
            elif file.get_mime_type() != 'application/pdf':
                return

        submenu = Nautilus.Menu()
        if len (files) < 2:
            itemc = Nautilus.MenuItem(
                name="CompressPdf::MenuItem",
                label="Compress PDF",
                tip="Compress PDF",
            )
            itemc.connect("activate", self.send_comp, files)
            return [itemc]
        item = Nautilus.MenuItem(
            name="CompressPdf::MenuItem",
            label="Compress and Merge PDF",
            tip="Compress and Merge PDF",
        )
        item.set_submenu(submenu)

        itosm = Nautilus.MenuItem(
            name="ToSmall::MenuItem",
            label="Compress PDF",
            tip="Compress PDF",
        )
        submenu.append_item(itosm)
        itosm.connect("activate", self.send_comp, files)
        comnmerge = Nautilus.MenuItem(
            name="MergenCompress::MenuItem",
            label="Compress and Merge PDF",
            tip="Compress and Merge PDF",
        )
        submenu.append_item(comnmerge)
        comnmerge.connect("activate", self.send_merge, files, '150')
        merge = Nautilus.MenuItem(
            name="MergePDF::MenuItem",
            label="Merge PDF",
            tip="Merge PDF",
        )
        submenu.append_item(merge)
        merge.connect("activate", self.send_merge, files, '300')
        return [item]

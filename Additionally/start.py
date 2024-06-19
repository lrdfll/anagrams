import os

from PyQt5 import QtCore, QtGui, QtWidgets


def get_icon(file_name):
    return QtGui.QIcon(os.path.join(QtWidgets.qApp.appDir, 'icons', file_name))


recent_doc_icon = get_icon('blue-folder-open-document-text.png')


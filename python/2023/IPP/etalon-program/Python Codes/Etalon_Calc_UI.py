#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 15:58:47 2023

@author: cdi
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QAction, qApp, QDesktopWidget, QTextEdit, QFileDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        #self.textEdit = QTextEdit()
        #self.setCentralWidget(self.textEdit)
        self.statusBar()
        self.filename = ''
        
        #select measured data
        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open New File')
        openFile.triggered.connect(self.fileDialog)
        
        label_filename = QLabel(self.filename, self)
        label_filename.setAlignment(Qt.AlignCenter)

        font1 = label_filename.font()
        font1.setPointSize(5)

        layout = QVBoxLayout()
        layout.addWidget(label_filename)
        
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(openFile)
        filemenu.addAction(exitAction)

        self.setWindowTitle('Icon')
        self.resize(500, 350)
        self.center()
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
    def fileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        self.filename = fname[0]
        label_filename = QLabel(self.filename, self)
        label_filename.setAlignment(Qt.AlignCenter)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
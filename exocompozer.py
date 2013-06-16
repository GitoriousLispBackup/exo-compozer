#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

from editors import newDotNormExo
from editors import newNormGraphExo

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except:
    print ("Error: This program needs PySide module.", file=sys.stderr)
    sys.exit(1)


class Compozer(QMainWindow):
    """ Display all exercices listed in save/ dir """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.createActions()
        self.createMenus()

        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Consmaster exercices composer")

        self.central_widget = self.createWidget()

        self.setCentralWidget(self.central_widget)

        self.populate()

        self.show()

    def createActions(self):
        self.quitAction = QAction("Quitter", self, triggered=self.close)
        self.createDotNormExo = QAction("New Norm->Dotted", self, \
                                         triggered=self.newDotNormExo)
        self.createNormGraphExo = QAction("New Norm->Graph", self, \
                                           triggered=self.newNormGraphExo)
        self.createGraphNormExo = QAction("New Graph->Norm", self, \
                                           triggered=self.newGraphNormExo)
        self.createFreeExo = QAction("New Free", self, \
                                      triggered=self.newFreeExo)
        self.removeExo = QAction("Remove Entry", self, \
                                      triggered=self.removeExo)

    def createMenus(self):
        menu = self.menuBar().addMenu("Menu")
        menu.addAction(self.createDotNormExo)
        menu.addAction(self.createNormGraphExo)
        menu.addAction(self.createGraphNormExo)
        menu.addAction(self.createFreeExo)
        menu.addSeparator()
        menu.addAction(self.removeExo)
        menu.addSeparator()
        menu.addAction(self.quitAction)

    def createWidget(self):
        """ Create main tab widget """
        # ~ widget = QWidget()

        tabWidget = QTabWidget()

        self.tabND = QTableWidget()  # ~ Normal - Dotted
        self.tabND.setColumnCount(2)
        self.tabND.setHorizontalHeaderLabels(["Exercice", "Difficulté"])
        self.tabND.setColumnWidth(1, 120)
        self.tabND.horizontalHeader().setResizeMode(0, QHeaderView.Stretch);
        self.tabND.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tabNG = QTableWidget()  # ~ Normal - Graph
        self.tabNG.setColumnCount(2)
        self.tabNG.setHorizontalHeaderLabels(["Exercice", "Difficulté"])
        self.tabNG.setColumnWidth(1, 120)
        self.tabNG.horizontalHeader().setResizeMode(0, QHeaderView.Stretch);
        self.tabNG.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tabGN = QTableWidget()  # ~ Graph - Normal
        self.tabGN.setColumnCount(2)
        self.tabGN.setHorizontalHeaderLabels(["Exercice", "Difficulté"])
        self.tabGN.setColumnWidth(1, 120)
        self.tabGN.horizontalHeader().setResizeMode(0, QHeaderView.Stretch);
        self.tabGN.setSelectionMode(QAbstractItemView.SingleSelection)

        tabWidget.addTab(self.tabND, "Normal - Dotted")
        tabWidget.addTab(self.tabNG, "Normal - Graph")
        tabWidget.addTab(self.tabGN, "Graph - Normal")

        self.tabND.itemDoubleClicked.connect(self.editExoND)
        self.tabNG.itemDoubleClicked.connect(self.editExoNG)
        self.tabGN.itemDoubleClicked.connect(self.editExoGN)

        # ~ widget.addWidget(tabWidget)
        return tabWidget

    def clearAll(self):
        self.tabND.clearContents()
        self.tabND.setRowCount(0)
        self.tabNG.clearContents()
        self.tabNG.setRowCount(0)
        self.tabGN.clearContents()
        self.tabGN.setRowCount(0)

    def populate(self):
        """ Populate tab widgets w/ files names """
        self.clearAll()
        for f in os.listdir("save/"):
            mode = f.split("_")[0]
            if mode == "NormDot":
                self.tabND.setRowCount(self.tabND.rowCount() + 1)
                self.tabND.setItem(self.tabND.rowCount() - 1, 0, \
                                    QTableWidgetItem(f.split("_")[1]))
            elif mode == "NormGraph":
                self.tabNG.setRowCount(self.tabNG.rowCount() + 1)
                self.tabNG.setItem(self.tabNG.rowCount() - 1, 0, \
                                    QTableWidgetItem(f.split("_")[1]))
            elif mode == "GraphNorm":
                self.tabGN.setRowCount(self.tabGN.rowCount() + 1)
                self.tabGN.setItem(self.tabGN.rowCount() - 1, 0, \
                                    QTableWidgetItem(f.split("_")[1]))

    def displayDifficulty(self):
        difficulty = 5
        text = ""
        for i in range(0, difficulty):
            if i % 2 == 0:
                text += "*"
        return text

    def removeExo(self):
        pass

    def editExoND(self, item):
        """ Modal autoloaded window for editing """
        newDotNormExo(self, item.text())

    def editExoNG(self, item):
        """ Modal autoloaded window for editing """
        newNormGraphExo(self, item.text())

    def editExoGN(self, item):
        """ Modal autoloaded window for editing """
        newGraphNormExo(self, item.text())

    def newDotNormExo(self):
        newDotNormExo(self)

    def newNormGraphExo(self):
        newNormGraphExo(self)

    def newGraphNormExo(self):
        pass

    def newFreeExo(self):
        pass


class newGraphNormExo(QDialog):
    pass

if __name__ == '__main__':

    app = QApplication(sys.argv)
    main = Compozer()
    sys.exit(app.exec_())

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except:
    print ("Error: This program needs PySide module.", file=sys.stderr)
    sys.exit(1)


class newDotNormExo(QDialog):
    """ Modal widget to create and edit Normal<->Dotted exercices """

    def __init__(self, parent, item=""):
        super().__init__(parent)

        self.setResult(0)
        self.finished.connect(parent.populate)

        self.setGeometry(300, 300, 500, 400)
        name_label = QLabel("Nom du fichier")
        self.name_field = QLineEdit()

        list_add_btn = QPushButton("Ajouter")
        list_rm_btn = QPushButton("Supprimer")
        list_add_btn.clicked.connect(self.add)
        list_rm_btn.clicked.connect(self.delete)

        ok_btn = QPushButton("Sauvegarder et quitter")
        ok_btn.clicked.connect(self.save)
        abort_btn = QPushButton("Annuler")
        abort_btn.clicked.connect(self.close)

        self.list_widget = self.listExo()

        layout = QGridLayout()
        layout.addWidget(name_label, 0, 0)
        layout.addWidget(self.name_field, 0, 1)
        layout.addWidget(self.list_widget, 5, 0, 1, 2)
        layout.addWidget(list_add_btn, 6, 0)
        layout.addWidget(list_rm_btn, 6, 1)
        layout.addWidget(ok_btn, 7, 0)
        layout.addWidget(abort_btn, 7, 1)

        self.setLayout(layout)

        if item is not "":
            self.load(item)

        self.setModal(True)
        self.exec_()

    def listExo(self):
        list_wid = QTableWidget()
        list_wid.setColumnCount(2)
        list_wid.setHorizontalHeaderLabels(["Dot", "Expression"])
        list_wid.setColumnWidth(0, 40)
        list_wid.horizontalHeader().setStretchLastSection(True)
        list_wid.setSortingEnabled(False)

        list_wid.setSelectionMode(QAbstractItemView.SingleSelection)
        list_wid.setEditTriggers(QAbstractItemView.AllEditTriggers)

        list_wid.itemChanged.connect(self.verify)

        return list_wid

    def add(self, value="None", state=Qt.Unchecked):
        """ Create an entry with nedeed flags """

        qi = QTableWidgetItem(value)
        qi.setFlags(Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        qdot = QTableWidgetItem()
        qdot.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        # ~ qdot.setFlags(Qt.ItemIsUserCheckable)
        qdot.setCheckState(state)
        qdot.setText("coucou")

        # ~ On ajoute une ligne
        # ~ Les rowCount ont un décalage de 1 Oo"
        self.list_widget.setRowCount(self.list_widget.rowCount() + 1)

        self.list_widget.setItem(self.list_widget.rowCount() - 1, 0, qdot)
        self.list_widget.setItem(self.list_widget.rowCount() - 1, 1, qi)

    def delete(self):
        self.list_widget.removeRow(self.list_widget.currentRow())

    def verify(self, item):
        # ~ Should check for valid lisp expr
        if (item.text() == "") and (item.column() == 1):
            item.setText("None")

    # ~ Cute iterator creator
    def iterAllItems(self):
        for i in range(self.list_widget.rowCount()):
            yield self.list_widget.item(i, 0), self.list_widget.item(i, 1)

    # ~ Save to file, need to be serialized
    def save(self):
        if self.name_field.text() is not "":
            if self.list_widget.rowCount() > 0:
                location = 'save/NormDot_{0}'.format(self.name_field.text())
                file = open(location, 'w+')
                try:
                    file.write("# Normal/Dotted serie\n")

                    for s, item in self.iterAllItems():
                        file.write("{0}\t{1}".format(s.checkState(), item.text()))
                        file.write("\n")
                finally:
                    file.close()
                self.done(1)

    # ~ Also need de-serial
    def load(self, exo):
        location = 'save/NormDot_{0}'.format(exo)
        self.name_field.setText(exo)
        try:
            file = open(location, 'r+')

            info = file.readline().rstrip('\n\r')

            for line in file:
                self.add(line.rstrip('\n\r').split("\t")[1])
        except IOError as e:
            print(e)
        finally:
            file.close()


class newNormGraphExo(QDialog):
    """ Modal widget to create and edit Normal->Graph exercices """

    def __init__(self, parent, item=""):
        super().__init__(parent)

        self.setResult(0)
        self.finished.connect(parent.populate)

        self.setGeometry(300, 300, 500, 400)
        name_label = QLabel("Nom du fichier")
        self.name_field = QLineEdit()

        list_add_btn = QPushButton("Ajouter")
        list_rm_btn = QPushButton("Supprimer")
        list_add_btn.clicked.connect(self.add)
        list_rm_btn.clicked.connect(self.delete)

        ok_btn = QPushButton("Sauvegarder et quitter")
        ok_btn.clicked.connect(self.save)
        abort_btn = QPushButton("Annuler")
        abort_btn.clicked.connect(self.close)

        self.list_widget = self.listExo()

        layout = QGridLayout()
        layout.addWidget(name_label, 0, 0)
        layout.addWidget(self.name_field, 0, 1)
        layout.addWidget(self.list_widget, 5, 0, 1, 2)
        layout.addWidget(list_add_btn, 6, 0)
        layout.addWidget(list_rm_btn, 6, 1)
        layout.addWidget(ok_btn, 7, 0)
        layout.addWidget(abort_btn, 7, 1)

        self.setLayout(layout)

        if item is not "":
            self.load(item)

        self.setModal(True)
        self.exec_()

    def listExo(self):
        list_wid = QTableWidget()
        list_wid.setColumnCount(1)
        list_wid.setHorizontalHeaderLabels(["Expression"])
        list_wid.horizontalHeader().setStretchLastSection(True)
        list_wid.setSortingEnabled(False)

        list_wid.setSelectionMode(QAbstractItemView.SingleSelection)
        list_wid.setEditTriggers(QAbstractItemView.AllEditTriggers)

        list_wid.itemChanged.connect(self.verify)

        return list_wid

    def add(self, value="None"):
        """ Create an entry with nedeed flags """

        qi = QTableWidgetItem(value)
        qi.setFlags(Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        self.list_widget.setRowCount(self.list_widget.rowCount() + 1)

        self.list_widget.setItem(self.list_widget.rowCount() - 1, 0, qi)

    def delete(self):
        self.list_widget.removeRow(self.list_widget.currentRow())

    def verify(self, item):
        # ~ Should check for valid lisp expr
        if (item.text() == ""):
            item.setText("None")

    # ~ Cute iterator creator
    def iterAllItems(self):
        for i in range(self.list_widget.rowCount()):
            yield self.list_widget.item(i, 0)

    # ~ Save to file, need to be serialized
    def save(self):
        if self.name_field.text() is not "":
            if self.list_widget.rowCount() > 0:
                location = 'save/NormGraph_{0}'.format(self.name_field.text())
                file = open(location, 'w+')
                try:
                    file.write("# Normal/Graph serie\n")

                    for item in self.iterAllItems():
                        file.write("{0}".format(item.text()))
                        file.write("\n")
                finally:
                    file.close()
                self.done(1)

    # ~ Also need de-serial
    def load(self, exo):
        location = 'save/NormGraph_{0}'.format(exo)
        self.name_field.setText(exo)
        try:
            file = open(location, 'r+')

            info = file.readline().rstrip('\n\r')

            for line in file:
                self.add(line.rstrip('\n\r'))
        except IOError as e:
            print(e)
        finally:
            file.close()
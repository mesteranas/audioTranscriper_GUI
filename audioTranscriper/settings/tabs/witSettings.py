import PyQt6.QtWidgets as qt
from PyQt6.QtCore import Qt
import gui,guiTools
class WitSettings(qt.QWidget):
    def __init__(self,p):
        super().__init__()
        self.languages=gui.witJsonControl.get()
        layout=qt.QVBoxLayout(self)
        self.currentLanguages=qt.QListWidget()
        self.currentLanguages.addItems(self.languages)
        self.currentLanguages.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.currentLanguages.customContextMenuRequested.connect(self.on_context)
        layout.addWidget(self.currentLanguages)
        self.add=qt.QPushButton(_("add"))
        self.add.clicked.connect(self.on_add)
        layout.addWidget(self.add)
    def on_add(self):
        choice,ok=qt.QInputDialog.getItem(self,_("select language"),_("language"),guiTools.dictionarys.languages.keys())
        if ok:
            key,ok=qt.QInputDialog.getText(self,_("inter your api key "),_("key"))
            if ok:
                self.languages[choice]=key
                self.currentLanguages.addItem(choice)
                gui.witJsonControl.save(self.languages)
    def on_context(self):
        ask=qt.QMessageBox.question(self,_("alert"),_("do you wanna delete this language"),qt.QMessageBox.StandardButton.Yes | qt.QMessageBox.StandardButton.No)
        if ask==qt.QMessageBox.StandardButton.Yes:
            try:
                del(self.languages[self.currentLanguages.currentItem().text()])
                gui.witJsonControl.save(self.languages)
                self.currentLanguages.clear()
                self.currentLanguages.addItems(self.languages)
            except:
                pass
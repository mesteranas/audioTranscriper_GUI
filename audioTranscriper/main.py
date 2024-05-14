import sys
from custome_errors import *
sys.excepthook = my_excepthook
import soundfile
import update
import gui
import guiTools
import speech_recognition as SR
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
class Thread(qt2.QThread):
    finish=qt2.pyqtSignal(str)
    def __init__(self,p,service,languageCodeOrApiKey,path):
        super().__init__(p)
        self.service=service
        self.LanguageCodeOrAPIKey=languageCodeOrApiKey
        self.path=path
    def run(self):
        try:
            data,sampleRate=soundfile.read(self.path)
            soundfile.write("data/result.wav",data,sampleRate)
            path="data/result.wav"
        except:
            path=self.path
        recognizer=SR.Recognizer()
        try:
            with SR.AudioFile(path) as SRC:
                audio=recognizer.record(SRC)
                text=""
                try:
                    if self.service==0:
                        text=recognizer.recognize_google(audio,language=self.LanguageCodeOrAPIKey)
                    elif self.service==1:
                        text=recognizer.recognize_wit(audio,self.LanguageCodeOrAPIKey)
                except Exception as error:
                    text=_("an error record")
        except:
            text="error"
        self.finish.emit(text)
class main (qt.QMainWindow ):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        layout=qt.QVBoxLayout()
        self.service=qt.QComboBox()
        self.service.addItems([_("google"),"wit.AI"])
        self.service.currentIndexChanged.connect(self.on_change_service)

        layout.addWidget(qt.QLabel(_("select service")))
        layout.addWidget(self.service)
        self.language=qt.QComboBox()
        layout.addWidget(qt.QLabel(_("select language")))
        layout.addWidget(self.language)
        self.path=qt.QLineEdit()
        self.path.setReadOnly(True)
        layout.addWidget(qt.QLabel(_("path")))
        layout.addWidget(self.path)
        self.browse=qt.QPushButton(_("browse"))
        self.browse.setDefault(True)
        self.browse.clicked.connect(self.on_browse)
        layout.addWidget(self.browse)
        self.convert=qt.QPushButton(_("convert to text"))
        self.convert.setDefault(True)
        self.convert.clicked.connect(self.on_convert)
        layout.addWidget(self.convert)
        self.result=qt.QLineEdit()
        self.result.setReadOnly(True)
        layout.addWidget(qt.QLabel(_("result")))
        layout.addWidget(self.result)
        self.on_change_service(0)
        self.setting=qt.QPushButton(_("settings"))
        self.setting.setDefault(True)
        self.setting.clicked.connect(lambda: settings(self).exec())
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

        mb=self.menuBar()
        help=mb.addMenu(_("help"))
        helpFile=qt1.QAction(_("help file"),self)
        help.addAction(helpFile)
        helpFile.triggered.connect(lambda:guiTools.HelpFile())
        helpFile.setShortcut("f1")
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/tprogrammers"))
        githup=qt1.QAction(_("Github"),self)
        cus.addAction(githup)
        githup.triggered.connect(lambda: guiTools.OpenLink(self,"https://Github.com/mesteranas"))
        X=qt1.QAction(_("x"),self)
        cus.addAction(X)
        X.triggered.connect(lambda:guiTools.OpenLink(self,"https://x.com/mesteranasm"))
        email=qt1.QAction(_("email"),self)
        cus.addAction(email)
        email.triggered.connect(lambda: guiTools.sendEmail("anasformohammed@gmail.com","project_type=GUI app={} version={}".format(app.name,app.version),""))
        Github_project=qt1.QAction(_("visite project on Github"),self)
        help.addAction(Github_project)
        Github_project.triggered.connect(lambda:guiTools.OpenLink(self,"https://Github.com/mesteranas/{}".format(settings_handler.appName)))
        Checkupdate=qt1.QAction(_("check for update"),self)
        help.addAction(Checkupdate)
        Checkupdate.triggered.connect(lambda:update.check(self))
        licence=qt1.QAction(_("license"),self)
        help.addAction(licence)
        licence.triggered.connect(lambda: Licence(self))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:guiTools.OpenLink(self,"https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
        if settings_handler.get("update","autoCheck")=="True":
            update.check(self,message=False)
    def closeEvent(self, event):
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()
    def on_change_service(self,index):
        self.language.clear()
        if index==0:
            self.language.addItems(guiTools.dictionarys.languages)
        elif index==1:
            self.language.addItems(gui.witJsonControl.get())
    def on_browse(self):
        file=qt.QFileDialog(self)   
        if file.exec()==file.DialogCode.Accepted:
            self.path.setText(file.selectedFiles()[0])
    def on_finish_converting(self,result):
        self.result.setText(result)
        self.result.setFocus()
    def on_convert(self):
        service=self.service.currentIndex()
        if service==0:
            languageOrApi=guiTools.dictionarys.languages[self.language.currentText()]
        elif service==1:
            languageOrApi=gui.witJsonControl.get()[self.language.currentText()]
        thread=Thread(self,self.service.currentIndex(),languageOrApi,self.path.text())
        thread.finish.connect(self.on_finish_converting)
        thread.start()
App=qt.QApplication([])
w=main()
w.show()
App.setStyle('fusion')
App.exec()
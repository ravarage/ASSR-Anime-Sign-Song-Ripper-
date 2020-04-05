from PyQt5 import QtWidgets,QtCore,QtGui
from tempfile import gettempdir
import sys
import os
import  subprocess
import configparser
import re
from frontdash import Ui_MainWindow as frontdashloader
from tagwindow import Ui_MainWindow as tagwindowloader
from setting import  Ui_MainWindow as settingloader
import threading
from selecter import Ui_MainWindow as selectorloader
loadedfiles = []
mkvfiles = []
assfiles = []
tagtokeep = []
createdfiles = []
mkvmergingdict = {}
tagtoremove = []
tagfound = []
mkvfilesload = []
from textbrowser import Ui_MainWindow as textbrowserloader
import traceback
from PyQt5.QtCore import pyqtSignal
#Stream #0:(\d*?):(.*)\n.*Metadata:|Stream #0:(.*?)\(.*\):(.*)\n.*Metadata:

cssbutton = "QPushButton {\n"
"    color: #444444;\n"
"    background: #F3F3F3;\n"
"    border: 1px #DADADA solid;\n"
"    padding: 5px 10px;\n"
"    border-radius: 2px;\n"
"    font-weight: bold;\n"
"    font-size: 20pt;\n"
"    outline: none;\n"
"}\n"
"\n"
"button:hover {\n"
"    border: 1px #C6C6C6 solid;\n"
"    box-shadow: 1px 1px 1px #EAEAEA;\n"
"    color: #333333;\n"
"    background: #F7F7F7;\n"
"}\n"
"\n"
"QPushButton:active {\n"
"    box-shadow: inset 1px 1px 1px #DFDFDF;   \n"
"}\n"
"\n"
"/* Blue button as seen on translate.google.com*/\n"
"QPushButton:blue {\n"
"    color: white;\n"
"    background: #4C8FFB;\n"
"    border: 1px #3079ED solid;\n"
"    box-shadow: inset 0 1px 0 #80B0FB;\n"
"}\n"
"\n"
"QPushButton:blue:hover {\n"
"    border: 1px #2F5BB7 solid;\n"
"    box-shadow: 0 1px 1px #EAEAEA, inset 0 1px 0 #5A94F1;\n"
"    background: #3F83F1;\n"
"}\n"
"\n"
"QPushButton:blue:active {\n"
"    box-shadow: inset 0 2px 5px #2370FE;   \n"
"}\n"
"\n"
"/* Orange button as seen on blogger.com*/\n"
"QPushButton:orange {\n"
"    color: white;\n"
"    border: 1px solid #FB8F3D; \n"
"    background: -webkit-linear-gradient(top, #FDA251, #FB8F3D);\n"
"    background: -moz-linear-gradient(top, #FDA251, #FB8F3D);\n"
"    background: -ms-linear-gradient(top, #FDA251, #FB8F3D);\n"
"}\n"
"\n"
"QPushButton:orange:hover {\n"
"    border: 1px solid #EB5200;\n"
"    background: -webkit-linear-gradient(top, #FD924C, #F9760B); \n"
"    background: -moz-linear-gradient(top, #FD924C, #F9760B); \n"
"    background: -ms-linear-gradient(top, #FD924C, #F9760B); \n"
"    box-shadow: 0 1px #EFEFEF;\n"
"}\n"
"\n"
"QPushButton:orange:active {\n"
"    box-shadow: inset 0 1px 1px rgba(0,0,0,0.3);\n"
"}\n"
"\n"
"/* Red Google Button as seen on drive.google.com */\n"
"QPushButton:red {\n"
"    background: -webkit-linear-gradient(top, #DD4B39, #D14836); \n"
"    background: -moz-linear-gradient(top, #DD4B39, #D14836); \n"
"    background: -ms-linear-gradient(top, #DD4B39, #D14836); \n"
"    border: 1px solid #DD4B39;\n"
"    color: white;\n"
"    text-shadow: 0 1px 0 #C04131;\n"
"}\n"
"\n"
"QPushButton:red:hover {\n"
"     background: -webkit-linear-gradient(top, #DD4B39, #C53727);\n"
"     background: -moz-linear-gradient(top, #DD4B39, #C53727);\n"
"     background: -ms-linear-gradient(top, #DD4B39, #C53727);\n"
"     border: 1px solid #AF301F;\n"
"}\n"
"\n"
"QPushButton:red:active {\n"
"     box-shadow: inset 0 1px 1px rgba(0,0,0,0.2);\n"
"    background: -webkit-linear-gradient(top, #D74736, #AD2719);\n"
"    background: -moz-linear-gradient(top, #D74736, #AD2719);\n"
"    background: -ms-linear-gradient(top, #D74736, #AD2719);\n"
"}\n"
"\n"
"\n"
"\n"
"/*=======================================*/\n"
"\n"
"body {\n"
"    margin: 50px;\n"
"}\n"
"\n"
"h1 {\n"
"    font: 150%/150% \'Freckle Face\', cursive;\n"
"}"


class WorkerSignals(QtCore.QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
class runable2(QtCore.QRunnable):
    def __init__(self, *args, **kwargs):
        super(runable2, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
    def anotherthread(self):

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        CREATE_NO_WINDOW = 0x08000000
        try:
            p = subprocess.run(self.args[0],shell=False,creationflags = CREATE_NO_WINDOW, startupinfo=startupinfo ,stdout=subprocess.PIPE)
            while True:
                text = ""

                for line in p.stdout.decode("UTF-8"):

                    text = text + line


                    if "Progress" in text and r"%" in text:
                        # self.setStatusTip(str(text))
                        regex = re.search(r"Progress:(.*)%", text)
                        try:
                            pass
                            self.signals.result.emit(regex.group(1))
                        except:
                            pass

                        text = ""
                else:
                    break
                if not line:
                    break


        except:
            pass
        else:
            pass
        finally:
            self.signals.finished.emit()

    def run(self):
        a  = threading.Thread(target=self.anotherthread)
        a.start()




class runable(QtCore.QRunnable):
    def __init__(self, *args, **kwargs):
        super(runable, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
    def anotherthread(self):

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        CREATE_NO_WINDOW = 0x08000000
        try:
            p = subprocess.run(self.args[0],shell=False,creationflags = CREATE_NO_WINDOW, startupinfo=startupinfo ,stdout=subprocess.PIPE)
            while True:
                text = ""
                for line in p.stdout.decode("UTF-8"):
                    text = text + line

                    if "Progress" in text and r"%" in text:
                        # self.setStatusTip(str(text))
                        regex = re.search(r"Progress:(.*)%", text)
                        try:
                            pass
                            self.signals.result.emit(regex.group(1))
                        except:
                            pass

                        text = ""
                else:
                    break
                if not line:
                    break


        except:
            pass
        else:
            pass
        finally:
            self.signals.finished.emit()

    def run(self):
        a  = threading.Thread(target=self.anotherthread)
        a.start()



class loadingwin(QtWidgets.QProgressBar):
    def __init__(self):
        super(loadingwin, self).__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(130, 140, 500, 125)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())



class textbrowserclass(QtWidgets.QMainWindow):
    tagfounds = []
    def tagreader(self,file):
        readlines = ""
        indexes = self.ui.treeWidget.selectionModel().selectedIndexes()

        try:
            ase = indexes[0].row()
        except:
            pass

        else:
            mes = self.ui.treeWidget.model().index(ase, 0)
            first_cell_selected = self.ui.treeWidget.model().data(mes, QtCore.Qt.DisplayRole)
            data = open(str(file), mode='r', encoding="utf-8")
            readdata = data.readlines()
            for line in readdata:
                regex = re.search(r"Dialogue:.*?,.*?,.*?,(.*?),", line)
                try:
                    tag = str(regex.group(1))
                except:
                    pass
                else:
                    if tag == first_cell_selected:
                        readline = re.search(r"^Dialogue:\s\d+,(\d+:\d+:\d+\.\d+),(\d+:\d+:\d+\.\d+),.*?,,.*?,.*?,.*?,,(.*)",line)
                        try:
                            start = readline.group(1)
                            end = readline.group(2)
                            text = readline.group(3)
                        except:
                            pass
                        else:
                            fullline = str(start) + ", " + str(end) + ", " + text + "\n"
                            readlines = readlines + fullline
        self.ui.textBrowser.setText(readlines)


    def tagfinder(self,file):
        data = open(str(file), mode='r', encoding="utf-8")
        readdata = data.readlines()
        for line in readdata:
            regex = re.search(r"Dialogue:.*?,.*?,.*?,(.*?),", line)
            try:
                tag = str(regex.group(1))
            except:
                pass
            else:
                if tag not in self.tagfounds:
                    self.tagfounds.append(tag)
                    item = QtWidgets.QTreeWidgetItem([tag,tag])
                    self.ui.treeWidget.addTopLevelItem(item)

    tagfound.sort()
    def __init__(self,file):
        super(textbrowserclass, self).__init__()
        self.ui = textbrowserloader()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('ico.png'))
        self.ui.treeWidget.setHeaderHidden(True)
        self.ui.treeWidget.hideColumn(0)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.tagfinder(file)
        self.ui.treeWidget.doubleClicked.connect(lambda :self.tagreader(file))

class settingclass(QtWidgets.QMainWindow):

    def savesetting(self):
        config['MKVToolNix location'] = {'dir': str(self.ui.lineEdit.text())}
        config['ffprobe location'] = {'dir': str(self.ui.lineEdit_2.text())}


        with open(asscconfig, 'w') as configfile:
            config.write(configfile)
        self.close()
    def location(self):
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open Directory')
        self.ui.lineEdit.setText(str(self.directory))
    def location2(self):
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open Directory')
        self.ui.lineEdit_2.setText(str(self.directory))

    def __init__(self):
        super(settingclass, self).__init__()
        self.ui = settingloader()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('ico.png'))
        self.ui.pushButton.setStyleSheet(cssbutton)
        self.ui.pushButton_2.setStyleSheet(cssbutton)
        self.ui.lineEdit.setStyleSheet(cssbutton)
        self.ui.lineEdit.setText(str(config['MKVToolNix location']['dir']))
        try:
            self.ui.lineEdit_2.setText(str(config['ffprobe location']['dir']))
        except:
            pass

        self.ui.pushButton.clicked.connect(self.location)
        self.ui.pushButton_3.clicked.connect(self.location2)

        self.ui.pushButton_2.clicked.connect(self.savesetting)


        self.setWindowModality(QtCore.Qt.ApplicationModal)
class tagtoremoveclass(QtWidgets.QMainWindow):
    def removetagtoremove(self):
        indexes = self.ui.treeWidget_2.selectionModel().selectedIndexes()

        try:
            ase = indexes[0].row()
        except:
            pass

        else:
            mes = self.ui.treeWidget_2.model().index(ase, 0)
            first_cell_selected = self.ui.treeWidget_2.model().data(mes, QtCore.Qt.DisplayRole)
            if str(first_cell_selected) != "dummy":
                tagfound.append(str(first_cell_selected))
                tagtoremove.remove(str(first_cell_selected))
                self.readdata()


    def addtoremove(self):
        indexes = self.ui.treeWidget.selectionModel().selectedIndexes()

        try:
            ase = indexes[0].row()
        except:
            pass

        else:
            mes = self.ui.treeWidget.model().index(ase, 0)
            first_cell_selected = self.ui.treeWidget.model().data(mes, QtCore.Qt.DisplayRole)
            if str(first_cell_selected) != "dummy":
                tagtoremove.append(str(first_cell_selected))
                tagfound.remove(str(first_cell_selected))
                self.readdata()


    def readdata(self):
        self.ui.treeWidget.clear()
        self.ui.treeWidget_2.clear()
        dummydata1  = QtWidgets.QTreeWidgetItem(["Dummy"])
        dummydata2  = QtWidgets.QTreeWidgetItem(["Dummy"])
        self.ui.treeWidget.addTopLevelItem(dummydata1)
        self.ui.treeWidget_2.addTopLevelItem(dummydata2)
        text1 = QtWidgets.QPushButton()
        text1.setText("Tag Found")
        self.ui.treeWidget.setItemWidget(dummydata1,1,text1)
        text2 = QtWidgets.QPushButton()
        text2.setText("Tag to remove")
        self.ui.treeWidget_2.setItemWidget(dummydata2,1,text2)
        for tag in tagfound:
            self.ui.treeWidget.addTopLevelItem(QtWidgets.QTreeWidgetItem([tag,tag]))
        for tags in tagtoremove:
            self.ui.treeWidget_2.addTopLevelItem(QtWidgets.QTreeWidgetItem([tags,tags]))





    def __init__(self):
        super(tagtoremoveclass, self).__init__()
        self.ui = tagwindowloader()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('ico.png'))
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ui.treeWidget.hideColumn(0)
        self.ui.treeWidget_2.hideColumn(0)
        self.ui.treeWidget.setHeaderHidden(True)
        self.ui.treeWidget_2.setHeaderHidden(True)
        self.readdata()
        self.ui.treeWidget.doubleClicked.connect(self.addtoremove)
        self.ui.treeWidget_2.doubleClicked.connect(self.removetagtoremove)

class tagtokeepclass(QtWidgets.QMainWindow):

    def removetagtokeep(self):
        indexes = self.ui.treeWidget_2.selectionModel().selectedIndexes()

        try:
            ase = indexes[0].row()
        except:
            pass

        else:
            mes = self.ui.treeWidget_2.model().index(ase, 0)
            first_cell_selected = self.ui.treeWidget_2.model().data(mes, QtCore.Qt.DisplayRole)
            if str(first_cell_selected) != "dummy":
                tagfound.append(str(first_cell_selected))
                tagtokeep.remove(str(first_cell_selected))
                self.readdata()


    def addtokeep(self):
        indexes = self.ui.treeWidget.selectionModel().selectedIndexes()

        try:
            ase = indexes[0].row()
        except:
            pass

        else:
            mes = self.ui.treeWidget.model().index(ase, 0)
            first_cell_selected = self.ui.treeWidget.model().data(mes, QtCore.Qt.DisplayRole)
            if str(first_cell_selected) != "dummy":
                tagtokeep.append(str(first_cell_selected))
                tagfound.remove(str(first_cell_selected))
                self.readdata()


    def readdata(self):
        self.ui.treeWidget.clear()
        self.ui.treeWidget_2.clear()
        dummydata1  = QtWidgets.QTreeWidgetItem(["Dummy"])
        dummydata2  = QtWidgets.QTreeWidgetItem(["Dummy"])
        self.ui.treeWidget.addTopLevelItem(dummydata1)
        self.ui.treeWidget_2.addTopLevelItem(dummydata2)
        text1 = QtWidgets.QPushButton()
        text1.setText("Tag Found")
        self.ui.treeWidget.setItemWidget(dummydata1,1,text1)
        text2 = QtWidgets.QPushButton()
        text2.setText("Tag to Keep")
        self.ui.treeWidget_2.setItemWidget(dummydata2,1,text2)
        for tag in tagfound:
            self.ui.treeWidget.addTopLevelItem(QtWidgets.QTreeWidgetItem([tag,tag]))
        for tags in tagtokeep:
            self.ui.treeWidget_2.addTopLevelItem(QtWidgets.QTreeWidgetItem([tags,tags]))





    def __init__(self):
        super(tagtokeepclass, self).__init__()
        self.ui = tagwindowloader()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('ico.png'))
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ui.treeWidget.hideColumn(0)
        self.ui.treeWidget_2.hideColumn(0)
        self.ui.treeWidget.setHeaderHidden(True)
        self.ui.treeWidget_2.setHeaderHidden(True)
        self.readdata()
        self.ui.treeWidget.doubleClicked.connect(self.addtokeep)
        self.ui.treeWidget_2.doubleClicked.connect(self.removetagtokeep)

class frontdashclass(QtWidgets.QMainWindow):


    def rippingdata(self):

        try:
            self.extracing.isAlive()
        except:
            try:
                self.rippingthread()
            except:pass
        else:
            while self.extracing.isAlive():
                QtWidgets.QMessageBox.about(self, "Warning",
                                            "Extracting Ass file from mkv files is not finished yet try again in a few")
            else:

                self.rippingthread()
    def checker(self):

        if len(self.done) == len(assfiles):
            QtWidgets.QMessageBox.about(self, "Done", "All operations are  completed")
            self.ui.treeWidget.clear()
            assfiles.clear()
            tagfound.clear()
            tagtoremove.clear()
            mkvmergingdict.clear()
            mkvfilesload.clear()
            mkvfiles.clear()
            self.done.clear()
            self.timer.stop()
        else:
            pass
    done = []
    def mergingthread(self,mkvstring):
        a = subprocess.run(mkvstring)
        self.done.append(mkvstring)
    u = 0
    def rippingthread(self):
        self.uu = 0
        QtWidgets.QMessageBox.about(self, "started", "All operations started wait till you get done signal")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.checker)
        self.timer.start(1000)
        self.loadingwindows=loadingwin()
        self.loadingwindows.hide()



        for file in assfiles:
            if file in mkvfilesload:
                self.loadingwindows.show()
                temp = gettempdir()
                newnewfile = temp + "\\" + str(self.u) + ".ass"
                self.u =+ 1
                createdfiles.append(newnewfile)
                try:
                    os.remove(newnewfile)
                except:
                    pass

                with open(str(file), mode='r', encoding="utf-8") as data:
                    for lines in data:
                        liness = re.search(r"Dialogue:.*?,.*?,.*?,(.*?),",lines)
                        try:
                            linetag = liness.group(1)
                        except:
                            linetag = "Not dialoge"
                        else:
                            linetag = liness.group(1)
                        if any(x == linetag for x in tagtoremove):

                            pass
                        else:
                            with open(str(newnewfile), mode='a', encoding="utf-8") as newdata:
                                newdata.write(lines)
                mkvfile = mkvmergingdict.get(file)
                mkvfilename = str(mkvfile)[int(str(mkvfile).rfind("/") + 1):]
                index = str(mkvfile).rfind(mkvfilename)
                folder = str(mkvfile[:index])
                outdir= '"' + folder + '/out"'
                if len(outdir) > 254:
                    outdir = '"'+ folder[0] + ":/ASSR" +'"'
                    QtWidgets.QMessageBox.about(self,"Warning","output folder exceed windows path limit \nOutput files will be in {}".format(outdir))



                try:
                    os.mkdir(outdir)
                except:
                    pass
                mkvnew = '"' + outdir + "/"+mkvfilename + '"'
                oldmkv = '"'+mkvfile +'"'
                newsub = '"' + newnewfile + '"'



                self.mkvmerge = str(config['MKVToolNix location']['dir']) + r"\mkvmerge"

                mkvstring = "{} -o {} {} --default-track 0 --track-name 0:ASSR {}  --default-language eng".format(self.mkvmerge,mkvnew, oldmkv, newsub)
                self.tgread = QtCore.QThreadPool()
                worker = runable2(mkvstring)
                worker.signals.result.connect(self.print_output)
                worker.signals.finished.connect(self.thread_complete2)
                self.tgread.start(worker)


            else:
                filename = str(file)[int(str(file).rfind("/") + 1):]
                index = str(file).rfind(filename)
                folder = str(file[:index])


                outputfolder = folder+ "ASSR Files"
                try:
                    os.mkdir(outputfolder)
                except:
                    pass

                newnewfile = outputfolder + "\\"+filename

                createdfiles.append(newnewfile)
                try:
                    os.remove(newnewfile)
                except:
                    pass

                with open(str(file), mode='r', encoding="utf-8") as data:
                    for lines in data:
                        if any(x in lines for x in tagtoremove):
                            pass
                        else:
                            with open(str(newnewfile), mode='a', encoding="utf-8") as newdata:
                                newdata.write(lines)




    def tagtoremoveloader(self):
        self.readingtagsfromass()
        self.tagtoremoveclass = tagtoremoveclass()
        self.tagtoremoveclass.show()
    def settingloader(self):

        self.settingclass = settingclass()
        self.settingclass.show()
    def tagtokeeploader(self):

        self.tagtokeepclass = tagtokeepclass()
        self.tagtokeepclass.show()
    #regex ^Style: (.*?)\,
    def readingtagsfromass(self):

        for i in assfiles:

            data =  open(str(i),mode='r',encoding="utf-8")
            readdata = data.readlines()
            for line in readdata:
                regex = re.search(r"Dialogue:.*?,.*?,.*?,(.*?),",line)
                try:
                    tag = str(regex.group(1))
                except:
                    pass
                else:
                    if  tag not in tagfound:
                        if tag not in tagtoremove:
                            tagfound.append(tag)
        tagfound.sort()


    def selectorwindow(self,text,numbers):
        self.windows = QtWidgets.QMainWindow()
        self.hui = selectorloader()
        self.hui.setupUi(self.windows)
        self.windows.setWindowTitle(text)

        for i in numbers:

            item = QtWidgets.QTreeWidgetItem([i,str(i)[int(str(i).rfind(",") + 1):]])
            self.hui.treeWidget.addTopLevelItem(item)
        self.windows.show()
        self.hui.treeWidget.hideColumn(0)
        self.hui.treeWidget.setHeaderHidden(True)
        self.hui.pushButton.clicked.connect(lambda :self.selectedsub(text))
        self.hui.treeWidget.doubleClicked.connect(lambda :self.selectedsub(text))

    def selectedsub(self,i):

        indexes = self.hui.treeWidget.selectionModel().selectedIndexes()

        try:
            ase = indexes[0].row()
        except:
            pass

        else:
            mes = self.hui.treeWidget.model().index(ase, 0)
            first_cell_selected = self.hui.treeWidget.model().data(mes, QtCore.Qt.DisplayRole)
            self.found.clear()
            self.found.append(first_cell_selected)
            self.windows.close()
            self.doingsomething(i, gettempdir())
    def textbrowserwin(self):
        indexes = self.ui.treeWidget.selectionModel().selectedIndexes()

        try:
            ase = indexes[0].row()
        except:
            pass

        else:
            mes = self.ui.treeWidget.model().index(ase, 0)
            first_cell_selected = self.ui.treeWidget.model().data(mes, QtCore.Qt.DisplayRole)
            self.textloader = textbrowserclass(first_cell_selected)
            self.textloader.show()



    def extraingassfrommkv(self):
        self.uu = 0
        self.loadingwindows=loadingwin()
        self.loadingwindows.hide()



        self.mkvinfo = str(config['MKVToolNix location']['dir']) + r"\mkvinfo"
        self.mkvextract = str(config['MKVToolNix location']['dir']) + r"\mkvextract"
        self.ffprobe = str(config['ffprobe location']['dir']) + r"\ffprobe"
        try:
            os.remove("batcher.bat")
        except:
            pass

        for i in mkvfiles:
            self.doit(i)






    def doit(self,i):
        temp = str(gettempdir())
        file = temp + "\\" + "temp.bat"
        outfile = temp + "\\" + "temp.txt"
        extractingstring = '{}  -loglevel error -select_streams s  -show_entries stream=index:stream -of _tags=language,title,codec_type -of csv=p=0  -i "{}" > {}'.format(
            self.ffprobe, i, outfile)
        with open(file, "w")as me:
            me.write(extractingstring)
            me.close()
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        CREATE_NO_WINDOW = 0x08000000

        subprocess.run([file], stderr=subprocess.PIPE,shell=False, creationflags=CREATE_NO_WINDOW, startupinfo=startupinfo)
       # p.communicate()
        self.found = []
        self.found.clear()
        with open(outfile) as ms:
            for ssa in ms:
                if "ass" in ssa.strip().lower():
                    if ssa not in self.found:
                        self.found.append(ssa.strip())
        if len(self.found) == 0:
            QtWidgets.QMessageBox.about(self, "Error", "No Subtitle found")
        if len(self.found) > 1:

            self.selectorwindow(i, self.found)

        else:

            self.doingsomething(i, temp)
    def print_output(self,a):
        try:
            e = len(mkvfiles) * 100
            b = self.uu * 100
            c = b + int(a)
            g = c /e
            k = g * 100
            k = int(k)
            self.loadingwindows.setValue(int(k))
        except:pass
    def thread_complete2(self):

        self.uu += 1
        if len(mkvfiles) == self.uu:
            self.loadingwindows.close()
            QtWidgets.QMessageBox.about(self,"Done","All merging mkv file done successfully")
    def thread_complete(self):

        self.uu += 1
        if len(mkvfiles) == self.uu:
            self.loadingwindows.close()
            QtWidgets.QMessageBox.about(self,"Done","All subtitle read successfully")
    def doingsomething(self,i,temp):
        self.loadingwindows.show()

        try:
            stream = self.found[0]
        except:
            QtWidgets.QMessageBox.about(self,"Error","no subtitle found")
        search = re.search(r"(\d*).", stream.strip())
        streamid = str(search.group(1)).strip()

        filename = str(i)[int(str(i).rfind("/") + 1):]
        newfile = '"'+temp + "\\" + filename + ".txt"+'"'
        newfiles = temp + "\\" +  filename + ".txt"

        forextract2 = '"' + self.mkvextract + '" '+'"' + i +'"'+ " tracks " + str(streamid) + ":" + newfile


        self.tgread = QtCore.QThreadPool()
        worker = runable(forextract2)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        self.tgread.start(worker)

       # self.extracing = threading.Thread(target=lambda: self.extractingthread(forextract2))
        #self.extracing.start()

        tempdict = {newfiles: i}
        mkvmergingdict.update(tempdict)

        if newfiles not in assfiles:
            assfiles.append(newfiles)
        if newfiles not in mkvfilesload:
            mkvfilesload.append(newfiles)
        self.ui.treeWidget.clear()

        for assfilee in assfiles:

            if str(mkvmergingdict.get(assfilee)) == None:
                assfile = assfilee
            else:
                assfile = str(mkvmergingdict.get(assfilee))


            startpoint = str(assfile).rfind("/")
            if startpoint == 0:
                startpoint = str(assfile).rfind("\\")
            if startpoint == 0:
                startpoint = str(assfile).rfind(r"\\")
            if startpoint == 0:
                self.ui.treeWidget.addTopLevelItem(QtWidgets.QTreeWidgetItem([assfile, assfile]))
            else:
                filenow = str(assfile)[startpoint + 1:]
                self.ui.treeWidget.addTopLevelItem(QtWidgets.QTreeWidgetItem([assfilee, filenow]))




    def removeselectedfile(self):
        tagfound.clear()
        tagtokeep.clear()
        tagtoremove.clear()

        indexes = self.ui.treeWidget.selectionModel().selectedIndexes()

        try:
            ase = indexes[0].row()
        except:
            pass

        else:
            mes = self.ui.treeWidget.model().index(ase, 0)
            first_cell_selected = self.ui.treeWidget.model().data(mes, QtCore.Qt.DisplayRole)
            if str(first_cell_selected) != "dummy":
                try:
                    assfiles.remove(str(first_cell_selected))
                except:pass
                else:
                    self.ui.treeWidget.clear()
                    dummydata = QtWidgets.QTreeWidgetItem(["Dummy", "Dummy"])

                    filename = QtWidgets.QPushButton(self.ui.centralwidget)
                    self.ui.treeWidget.addTopLevelItem(dummydata)

                    filename.setStyleSheet(cssbutton)
                    filename.setText("Files")
                    filename.setFont(QtGui.QFont("a", 15))
                    self.ui.treeWidget.setItemWidget(dummydata, 1, filename)
                    for assfile in assfiles:
                        startpoint = str(assfile).rfind("/")
                        if startpoint == 0:
                            self.ui.treeWidget.addTopLevelItem(QtWidgets.QTreeWidgetItem([assfile, assfile]))
                        else:
                            filenow = str(assfile)[startpoint + 1:]
                            self.ui.treeWidget.addTopLevelItem(QtWidgets.QTreeWidgetItem([assfile, filenow]))

    def examingfiles(self):
        self.ui.treeWidget.clear()
        for file in loadedfiles:
            if str(file).endswith("mkv"):
                if file not in mkvfiles:

                    mkvfiles.append(str(file))


            elif str(file).endswith("ass"):
                if file not in assfiles:
                    assfiles.append(str(file))
                for assfile in assfiles:
                    startpoint = str(assfile).rfind("/")

                    if startpoint == 0:
                        self.ui.treeWidget.addTopLevelItem(QtWidgets.QTreeWidgetItem([assfile, assfile]))
                    else:
                        filenow = str(assfile)[startpoint + 1:]
                        self.ui.treeWidget.addTopLevelItem(QtWidgets.QTreeWidgetItem([assfile, filenow]))


    def creatingdir(self):
        pass

    #  directory = str(QtWidgets.QFileDialog.getExistingDirectory())
    def loadfolder(self):
        tagfound.clear()
        tagtokeep.clear()
        tagtoremove.clear()
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open Directory')

        try:
            os.listdir(self.directory)
        except:pass
        else:
            if int(self.finder() == 1):
                for i in os.listdir(self.directory):
                    if i.endswith("ass") or i.endswith("mkv"):
                        file = self.directory + "/" + i
                        loadedfiles.append(file)
            else:
                for i in os.listdir(self.directory):
                    if i.endswith("ass"):
                        file = self.directory + "/" + i
                        loadedfiles.append(file)
            self.examingfiles()

            self.extraingassfrommkv()




        #self.creatingdir()




    def loadfiles(self):
        tagfound.clear()
        tagtokeep.clear()
        tagtoremove.clear()
        options = QtWidgets.QFileDialog.Options()
        if int(self.finder() == 1):
            files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                              "Supported files Files (*.mkv *.ass);;Ass Subtitles (*.ass);;Matroska Files (*.mkv);;All Files (*)",
                                                              options=options)
        else:
            files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                              "Ass Subtitles (*.ass);;All Files (*)",
                                                              options=options)

        if files:
            for file in files:
                if file not in loadedfiles:
                    loadedfiles.append(file)
            self.ui.treeWidget.clear()

            self.creatingdir()

            self.examingfiles()

            self.extraingassfrommkv()

    def __init__(self):
        super(frontdashclass, self).__init__()
        self.ui = frontdashloader()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('ico.png'))
        self.showMaximized()

        dummydata = QtWidgets.QTreeWidgetItem(["Dummy","Dummy"])
        self.ui.treeWidget.addTopLevelItem(dummydata)
        self.ui.treeWidget.setHeaderHidden(True)
        self.ui.treeWidget.hideColumn(0)
        filename = QtWidgets.QPushButton(self.ui.centralwidget)
        self.ui.treeWidget.doubleClicked.connect(self.textbrowserwin)
        filename.setStyleSheet(cssbutton)
        filename.setText("Files")

        filename.setFont(QtGui.QFont("a",15))
        self.ui.treeWidget.setFont(QtGui.QFont("a",15))
        self.ui.treeWidget.setItemWidget(dummydata, 1, filename)
        self.ui.pushButton.clicked.connect(self.loadfiles)
        self.ui.pushButton_2.clicked.connect(self.loadfolder)
        self.mkvinfo = str(config['MKVToolNix location']['dir']) + r"\mkvinfo"
        self.mkvextract = str(config['MKVToolNix location']['dir']) + r"\mkvextract"


        self.ui.pushButton_6.clicked.connect(self.tagtokeeploader)
        self.ui.pushButton_7.clicked.connect(self.tagtoremoveloader)
        self.ui.pushButton_3.clicked.connect(self.removeselectedfile)
        self.ui.pushButton_5.clicked.connect(self.rippingdata)
        self.ui.pushButton_4.clicked.connect(self.settingloader)
        self.setStatusTip("Ready")

      #  self.load.changevalue(45)




        self.ui.pushButton_6.hide()
        mkvextract = str(config['MKVToolNix location']['dir'])
        ffprobe = str(config['ffprobe location']['dir'])
        try:
            oss = os.listdir(mkvextract)
        except:

            QtWidgets.QMessageBox.about(self, "error", "Mkvtoolnix not found please specify location in setting")

        else:

            if "mkvextract.exe" in oss:

                pass
            else:
                QtWidgets.QMessageBox.about(self, "error",
                                            "mkvextract not found please make sure all mkvtoonix tools are in on folder")

            if "mkvmerge.exe" in oss:
                try:
                    ossp = os.listdir(ffprobe)
                except:
                    QtWidgets.QMessageBox.about(self, "error",
                                                "mkvmerge not found please specify location in setting")


                else:
                    if "ffprobe.exe" in ossp:

                        pass
                    else:
                        QtWidgets.QMessageBox.about(self, "error",
                                                    "ffprobe not found please make sure its names ffprobe.exe and specify it location in setting")


            else:
                QtWidgets.QMessageBox.about(self, "error",
                                            "mkvmerge not found please make sure all mkvtoonix tools are in on folder")



    def finder(self):
        mkvextract = str(config['MKVToolNix location']['dir'])
        ffprobe = str(config['ffprobe location']['dir'])
        try:
            oss = os.listdir(mkvextract)
        except:


            return 0
        else:

            if "mkvextract.exe" in oss:

                pass
            else:

                return 0
            if "mkvmerge.exe" in oss:
                try:
                    ossp = os.listdir(ffprobe)
                except:

                    return 0

                else:
                    if "ffprobe.exe" in ossp:
                        return 1

                    else:
                        return 0

            else:
                return 0




def handler(msg_type, msg_log_context, msg_string):
    pass
    #print(msg_type, msg_log_context, msg_string)
QtCore.qInstallMessageHandler(handler)
if __name__ == "__main__":
    config = configparser.ConfigParser()
    settinglocation = str(os.path.expanduser("~\\")) + str(r"ASSR Setting\\")
    try:
        os.mkdir(settinglocation)
    except:pass
    asscconfig = settinglocation + "asscconfig.ini"

    config.read(asscconfig)
    if "asscconfig.ini" not in os.listdir(settinglocation):

        config['MKVToolNix location'] = {'dir':"C:\Program Files\MKVToolNix"}

        with open(asscconfig, 'w') as configfile:
            config.write(configfile)


    with open('asscconfig.ini', 'w') as fout:
        config.write(fout)

    app = QtWidgets.QApplication(sys.argv)
    application = frontdashclass()
    application.show()

    sys.exit(app.exec_())


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
        QtWidgets.QMessageBox.about(self, "started", "All operations started wait till you get done signal")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.checker)
        self.timer.start(1000)


        for file in assfiles:
            if file in mkvfilesload:
                print("Got hre")
                temp = gettempdir()

                newnewfile = temp + "\\" + str(self.u) + ".ass"
                self.u =+ 1
                print(newnewfile)

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
                mkvfile = mkvmergingdict.get(file)
                mkvfilename = str(mkvfile)[int(str(mkvfile).rfind("/") + 1):]
                index = str(mkvfile).rfind(mkvfilename)
                folder = str(mkvfile[:index])
                print(index,folder,mkvfilename[:-4])
                mkvnew = '"' + folder + mkvfilename + 'AS.mkv"'
                oldmkv = '"'+mkvfile +'"'
                newsub = '"' + newnewfile + '"'



                self.mkvmerge = str(config['MKVToolNix location']['dir']) + r"\mkvmerge"

                mkvstring = "{} -o {} {}  --track-name 0:ASSR {}  --default-language eng".format(self.mkvmerge,mkvnew, oldmkv, newsub)
                thread = threading.Thread(target=(lambda :self.mergingthread(mkvstring)))
                thread.start()


                "mkvmerge -o output.mkv input.mkv subs.srt"

            else:
                filename = str(file)[int(str(file).rfind("/") + 1):]
                index = str(file).rfind(filename)
                folder = str(file[:index])
                print("Wront folder")

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
            print(i)
            data =  open(str(i),mode='r',encoding="utf-8")
            readdata = data.readlines()
            for line in readdata:
                regex = re.search(r"^Style: (.*?)\,", str(line))
                try:
                    tag = str(regex.group(1))
                except:
                    pass
                else:
                    if  tag not in tagfound:
                        if tag not in tagtoremove:
                            tagfound.append(tag)




    def extractingthread(self,forextract2):
        try:
            p = subprocess.run(forextract2, shell=True)
        except:pass
        else: pass

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

    def extraingassfrommkv(self):



        self.mkvinfo = str(config['MKVToolNix location']['dir']) + r"\mkvinfo"
        self.mkvextract = str(config['MKVToolNix location']['dir']) + r"\mkvextract"
        self.ffprobe = str(config['ffprobe location']['dir']) + r"\ffprobe"
        try:
            os.remove("batcher.bat")
        except:
            pass

        for i in mkvfiles:
            self.doit(i)

    def timerother(self,i):
        self.timer2.stop()
        self.doit(i)


    def doit(self,i):
        try:
            self.extracing.is_alive()
        except:
            self.doitt(i)
        else:
            if self.extracing.is_alive():
                self.timer2 = QtCore.QTimer()
                self.timer2.timeout.connect(lambda :self.timerother(i))
                self.timer2.start(1000)

            else:
                self.doitt(i)
    def doitt(self,i):
        temp = str(gettempdir())
        file = temp + "\\" + "temp.bat"
        outfile = temp + "\\" + "temp.txt"
        extractingstring = '{}  -loglevel error -select_streams s  -show_entries stream=index:stream -of _tags=language,title,codec_type -of csv=p=0  -i "{}" > {}'.format(
            self.ffprobe, i, outfile)
        with open(file, "w")as me:
            me.write(extractingstring)
            me.close()
        p = subprocess.Popen([file], stderr=subprocess.PIPE)
        p.communicate()
        self.found = []
        self.found.clear()
        with open(outfile) as ms:
            for ssa in ms:
                if "ass" in ssa.strip().lower():
                    self.found.append(ssa.strip())
        if len(self.found) == 0:
            QtWidgets.QMessageBox.about(self, "Error", "No Subtitle found")
        if len(self.found) > 1:

            self.selectorwindow(i, self.found)

        else:

            self.doingsomething(i, temp)

    def doingsomething(self,i,temp):

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
        print(forextract2,"gg")

        self.extracing = threading.Thread(target=lambda: self.extractingthread(forextract2))
        self.extracing.start()

        tempdict = {newfiles: i}
        mkvmergingdict.update(tempdict)
        print(newfiles)
        assfiles.append(newfiles)
        mkvfilesload.append(newfiles)
        self.ui.treeWidget.clear()

        for assfile in assfiles:
            startpoint = str(assfile).rfind("/")

            if startpoint == 0:
                self.ui.treeWidget.addTopLevelItem(QtWidgets.QTreeWidgetItem([assfile, assfile]))
            else:
                filenow = str(assfile)[startpoint + 1:]
                self.ui.treeWidget.addTopLevelItem(QtWidgets.QTreeWidgetItem([assfile, filenow]))




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
        print(self.directory)
        for i in os.listdir(self.directory):
            if i.endswith("ass") or i.endswith("mkv"):

                file = self.directory + "/" + i
                loadedfiles.append(file)
        self.creatingdir()


        self.examingfiles()

        self.extraingassfrommkv()

    def loadfiles(self):
        tagfound.clear()
        tagtokeep.clear()
        tagtoremove.clear()
        options = QtWidgets.QFileDialog.Options()
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "Supported files Files (*.mkv *.ass);;Ass Subtitles (*.ass);;Matroska Files (*.mkv);;All Files (*)", options=options)
        if files:
            for file in files:
                if file not in loadedfiles:
                    loadedfiles.append(file)

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

        filename.setStyleSheet(cssbutton)
        filename.setText("Files")
        filename.setFont(QtGui.QFont("a",15))
        self.ui.treeWidget.setFont(QtGui.QFont("a",15))
        self.ui.treeWidget.setItemWidget(dummydata, 1, filename)
        self.ui.pushButton.clicked.connect(self.loadfiles)
        self.ui.pushButton_2.clicked.connect(self.loadfolder)
        self.mkvinfo = str(config['MKVToolNix location']['dir']) + r"\mkvinfo"
        self.mkvextract = str(config['MKVToolNix location']['dir']) + r"\mkvextract"
        print(self.mkvinfo)

        self.ui.pushButton_6.clicked.connect(self.tagtokeeploader)
        self.ui.pushButton_7.clicked.connect(self.tagtoremoveloader)
        self.ui.pushButton_3.clicked.connect(self.removeselectedfile)
        self.ui.pushButton_5.clicked.connect(self.rippingdata)
        self.ui.pushButton_4.clicked.connect(self.settingloader)



        self.ui.pushButton_6.hide()


def handler(msg_type, msg_log_context, msg_string):
    print(msg_type, msg_log_context, msg_string)
QtCore.qInstallMessageHandler(handler)
if __name__ == "__main__":
    config = configparser.ConfigParser()
    settinglocation = str(os.path.expanduser("~\\")) + str(r"ASSR Setting\\")
    try:
        os.mkdir(settinglocation)
    except:pass
    asscconfig = settinglocation + "asscconfig.ini"
    print(asscconfig)
    config.read(asscconfig)
    if "asscconfig.ini" not in os.listdir(settinglocation):
        print("stanwa")
        config['MKVToolNix location'] = {'dir':"C:\Program Files\MKVToolNix"}

        with open(asscconfig, 'w') as configfile:
            config.write(configfile)


    print(config['MKVToolNix location']['dir'])
    with open('asscconfig.ini', 'w') as fout:
        config.write(fout)
    app = QtWidgets.QApplication(sys.argv)
    application = frontdashclass()
    application.show()
    sys.exit(app.exec_())


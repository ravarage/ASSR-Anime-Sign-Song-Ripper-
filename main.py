import mpv
import pysubs2
from PyQt5 import QtWidgets,QtCore,QtGui
from tempfile import gettempdir
import sys
import os
from time import strftime,gmtime
from textbrowsers import Ui_MainWindow as textbrowserloaders
import threading
from PyQt5.QtCore import pyqtSignal
class contriner(QtWidgets.QWidget):
    def __init__(self,*args,**kwargs):
        super(contriner, self).__init__()
        self.signals = WorkerSignals()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.signals.finished.emit()
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
class textbrowserclass(QtWidgets.QMainWindow):
    tagfounds = []
    def tagreader(self,file):
        self.tree.clear()
        readlines = ""
        indexes = self.ui.treeWidget.selectionModel().selectedIndexes()

        try:
            ase = indexes[0].row()
        except:
            pass

        else:
            mes = self.ui.treeWidget.model().index(ase, 0)
            first_cell_selected = self.ui.treeWidget.model().data(mes, QtCore.Qt.DisplayRole)
            data =pysubs2.load(str(file))

            for line in data:
                tag = str(line.style).strip()
                if tag == first_cell_selected:
                    start = str(strftime("%H:%M:%S", gmtime(line.start/1000)))
                    end = str(strftime("%H:%M:%S", gmtime(line.end/1000)))
                    text = str(line.text)
                    item = QtWidgets.QTreeWidgetItem([first_cell_selected,start,str(line.start),end,text])
                    self.tree.addTopLevelItem(item)



        try:
            self.tree.disconnect()
        except:
            pass
        if str(self.mkv).endswith("ass"):
            pass
        else:
            self.tree.doubleClicked.connect(self.gototime)
    def gototime(self):
        indexes = self.tree.selectedIndexes()

        try:
            ase = indexes[0].row()
        except:
            pass

        else:
            mes = self.tree.model().index(ase, 0)
            tagstyle = self.tree.model().data(mes, QtCore.Qt.DisplayRole)
            mes1 = self.tree.model().index(ase, 2)
            start = self.tree.model().data(mes1, QtCore.Qt.DisplayRole)
            data = pysubs2.load(str(self.file))

            for line in data:
                tag = str(line.style).strip()
                if tag == tagstyle:
                    pass
                else:
                    line.text == ""
            temp = str(gettempdir())
            tempass = temp + "\\" + "temptag.ass"
            data.save(tempass)

            self.player.command(r'sub-add', tempass,"select")



        time = str((int(start)/1000)-0.1)
        self.player.seek(time, reference='absolute', precision='exact')
        try:
            self.player._set_property("pause",False)
        except:
            QtWidgets.QMessageBox.about(self,"Error","subtile start after movie ended so no preview")
    def stoptime(self):
        self.player.command("cycle", "pause")

    def tagfinder(self,file):
        data = pysubs2.load(str(file))


        for line in data:
            tag = str(line.style).strip().strip()

            if tag not in self.tagfounds:
                self.tagfounds.append(tag)
                item = QtWidgets.QTreeWidgetItem([tag, tag])
                self.ui.treeWidget.addTopLevelItem(item)
        self.tagfounds.sort()


    def anotherthread(self,e,file):


        self.player = mpv.MPV(wid=str(int(e)), log_handler=print)


        self.player.command('loadfile', file)

       
        self.player.wait_for_property('seekable')



        self.player.show_progress()


    def __init__(self,file,mkv):
        self.tagfounds.clear()
        super(textbrowserclass, self).__init__()
        self.ui = textbrowserloaders()
        self.ui.setupUi(self)
        self.file =file
        self.mkv = mkv
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setWindowIcon(QtGui.QIcon('ico.png'))
        self.ui.treeWidget.setHeaderHidden(True)
        self.ui.treeWidget.hideColumn(0)
        self.ui.textBrowser.hide()
        self.tree = QtWidgets.QTreeWidget(self.ui.centralwidget)
        self.ui.gridLayout.addWidget(self.tree,0,1,1,1)
        self.tagfinder(file)

        self.ui.treeWidget.doubleClicked.connect(lambda :self.tagreader(file))
        self.tagfinder(file)
        self.ui.textEdit.close()
        self.tree.headerItem().setText(0,  "tag")
        self.tree.headerItem().setText(1, "Start")
        self.tree.headerItem().setText(2, "hidden Start")

        self.tree.headerItem().setText(3, "End")
        self.tree.headerItem().setText(4, "Text")
        self.tree.hideColumn(0)
        self.tree.hideColumn(2)

        self.tree.setColumnWidth(1,60)
        self.tree.setColumnWidth(3,60)



        self.container = contriner(self)
        # self.setCentralWidget(self.container)
        if str(mkv).endswith("ass"):
            pass
        else:
            self.container.signals.finished.connect(self.stoptime)
            self.container.setAttribute(QtCore.Qt.WA_DontCreateNativeAncestors)
            self.container.setAttribute(QtCore.Qt.WA_NativeWindow)
            self.ui.gridLayout.addWidget(self.container, 1, 0, 1, 2)

            self.container.setMinimumHeight(350)
            self.container.setMinimumWidth(800)
            a = int(self.container.winId())
            self.another = threading.Thread(target=lambda: self.anotherthread(a, mkv))

            self.another.start()

if __name__ == '__main__':
    apps = QtWidgets.QApplication(sys.argv)
    #a = sys.argv

    a = ["","a.ass",r"C:\assctemp\PycharmProjects\New folder\2.mkv"]
    #a = ["","a.ass",r"a.ass"]

    textloader = textbrowserclass(str(a[1]),str(a[2]))
    textloader.show()
    sys.exit(apps.exec_())


# coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from saveCssImg import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class UI_getImg(QtGui.QDialog):    
    def __init__(self, parent=None):
        super(UI_getImg, self).__init__(parent)  
        self.setupUi(self) 
        self.lineEdit.setText('http://simg.sinajs.cn/blog7style/css/conf/blog/article.css') 
        self.textBrowser.setOpenExternalLinks(True) 
        self.textBrowser.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textBrowser.setStyleSheet("QTextBrowser {background: #eee; }")
        self.pushButton.clicked.connect(self.goWork) 
    
    def goWork(self):
        self.thread = WorkerThread()
        self.thread.sinOut[unicode].connect(self.outText)
        self.thread.sinOut[tuple].connect(self.outText)
        self.thread.finished.connect(self.workFinished)

        cssUrl = str(self.lineEdit.text())
        savePath = 'downImgs'

        self.textBrowser.setText(u'CSS文件地址: <a href="%s">%s</a><br>__________<br>' %  (cssUrl,cssUrl))
        self.pushButton.setDisabled(True)

        self.thread.setEvr(cssUrl,savePath)

    def outText(self,info):
        if isinstance(info,tuple):
            self.textBrowser.append(u'有%s个下载失败' % info[1])
        else:
            self.textBrowser.append(info)

    def workFinished(self):
        self.outText(u'<br>__________<br>已退出下载！')
        self.pushButton.setDisabled(False)


    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(800, 407)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(700, 20, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.textBrowser = QtGui.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(10, 60, 780, 341))        
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(10, 20, 670, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))        

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "下载Css文件图片", None))
        self.pushButton.setText(_translate("Dialog", "下载", None))   

class WorkerThread(QtCore.QThread):
    sinOut = QtCore.pyqtSignal([unicode],[tuple])
     
    def __init__(self,parent=None):
        super(WorkerThread,self).__init__(parent)

    def setEvr(self,cssUrl,savePath):
        self.cssUrl = cssUrl
        self.savePath = savePath
        self.start()

    def outInfo(self,info):
        if isinstance(info,unicode) :
            self.sinOut[unicode].emit(info)
        else:
            self.sinOut[tuple].emit(info)

    def run(self):
        self.saveimg = saveCssBackImg(self.cssUrl,self.savePath,self.outInfo)
        self.saveimg.saveImg()

if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    ui = UI_getImg()
    ui.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
    ui.show()
    app.exec_()
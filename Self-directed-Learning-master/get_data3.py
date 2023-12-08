import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Kiwoom Login
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

        #OpenAPI+Event
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

        self.setWindowTitle("계좌정보")
        self.setGeometry(300, 300, 300, 150)
        #ProgID를 QAxWidget 클래스의 생성자로 전달하여 인스턴스를 생성합니다.
        
        btn1 = QPushButton("계좌얻기", self)
        btn1.move(190, 20)
        btn1.clicked.connect(self.btn1_clicked)
 
        def btn1_clicked(self):
            account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
            self.text_edit.append("계좌번호: "+account_num.rstrip(';'))

        def event_connect(self, err_code):
            if err_code == 0:
                self.text_edit.append("로그인 성공")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
            
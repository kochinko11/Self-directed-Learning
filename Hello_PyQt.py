import sys # import 모듈명 으로 모듈을 임포트
from PyQt5.QtWidgets import * #PyAt5라는 디렉터리의 QtWidgets 파일에 있는 모든것을 import 하라는 의미

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 400)

if __name__ == "__main__":
    app = QApplication(sys.argv) #QApplication 클래스에 대한 인스턴스를 생성하고 app이라는 변수로 바인딩
    #print(sys.argv) // 현재 소스코드에 대한 절대경로. QA클래스의 인스턴스를 생성할 때 생성자로 이 값을 전달해야함
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()#app을 통해 exec_ 메서드를 호출하면 이벤트 루프에 진입
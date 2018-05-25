#블록체인을 위하여
import hashlib as hasher
import datetime as date

#pyqt5를 사용하여 gui사용
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QStandardItem, QStandardItemModel


#Ui를 정의하고 있는 클래스
class Ui_Form(object):
    blockchain = []
    previous_block = []
    block_to_add = []


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 500)#사이즈 변경
        self.addBtn = QtWidgets.QPushButton(Form)
        self.addBtn.setGeometry(QtCore.QRect(50, 150, 75, 23))
        self.addBtn.setObjectName("addBtn")
        self.date_textBox = QtWidgets.QLineEdit(Form)
        self.date_textBox.setGeometry(QtCore.QRect(50, 10, 350, 20))
        self.date_textBox.setObjectName("date_textBox")
        self.use_textBox = QtWidgets.QLineEdit(Form)
        self.use_textBox.setGeometry(QtCore.QRect(50, 30, 350, 20))
        self.use_textBox.setObjectName("use_textBox")
        self.cause_textBox = QtWidgets.QLineEdit(Form)
        self.cause_textBox.setGeometry(QtCore.QRect(50, 50, 350, 20))
        self.cause_textBox.setObjectName("cause_textBox")


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "This is Widget"))
        self.addBtn.setText(_translate("Form", "ADD"))
        self.addBtn.clicked.connect(self.add_btn_clicked)

    #add 클릭하였을 때 일어나는 일
    def add_btn_clicked(self):
        date = self.date_textBox.text()
        use_money = self.use_textBox.text()
        cause = self.cause_textBox.text()

        if len(self.blockchain) == 0:#블록의 길이가 0이면
            # 맨 처음 블록 생성 후 체인으로 블록 묶기
            self.blockchain = [create_genesis_block()]  # 리스트인 blockchanin에 첫번째 값(genesis) 블록 넣음
            self.previous_block = self.blockchain[0]  # 위에서 생성된 첫번째 블록 만듬

            if date:
                self.block_to_add = next_block(self.previous_block, date, use_money, cause)  # next_block사용하여 블록 생성
                self.blockchain.append(self.block_to_add)  # 맨 처음 붙인 블록에 위에 만든 블록 붙임(리스트임)
                self.previous_block = self.block_to_add  # 전의 블록은 위에 생성된 블록으로 바꿈

                print(date, ' ', use_money, ' ', cause)
        else:
            if date:
                block_to_add = next_block(self.previous_block, date, use_money, cause)  # next_block사용하여 블록 생성
                self.blockchain.append(block_to_add)  # 맨 처음 붙인 블록에 위에 만든 블록 붙임(리스트임)
                self.previous_block = block_to_add  # 전의 블록은 위에 생성된 블록으로 바꿈

                print(date, ' ', use_money, ' ', cause)

#블록 정의
class Block:
    def __init__(self, index, timestamp, ormoney, usemoney, remoney, cause,  previous_hash):
        self.index = index #번호
        self.timestamp = timestamp #시간
        self.ormoney = ormoney #원래 있었던 돈
        self.usemoney = usemoney #사용한 돈
        self.remoney = remoney #남은 돈
        self.cause = cause #사용 이유
        self.previous_hash = previous_hash #전에 있던 블록
        self.hash = self.hash_block()

        #암호화
    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + str(self.ormoney).encode(
            'utf-8') + str(self.usemoney).encode('utf-8') + str(self.remoney).encode('utf-8') + str(self.usemoney).encode(
            'utf-8') + str(self.cause).encode('utf-8') + str(self.previous_hash).encode('utf-8'))

        return sha.hexdigest()


# 남은 금액 반환하는 함수
def getRemainmoney(ormoney, usemoney):
    return ormoney - usemoney


# 맨 처음 블록 생성하는 함수
def create_genesis_block():
    return Block(0, date.datetime.now(), 100000, 0, getRemainmoney(100000, 0), '', "0")


# 다음 블록 생성하는 함수
def next_block(last_block, day, usemoney, cause):
    this_index = last_block.index + 1
    this_timestamp = day
    this_ormoney = last_block.remoney  # 전에 남은 금액이 현재 있는 돈이 된다
    this_usemoney = usemoney  # 사용한 금액을 매개변수로 받아서 저장
    this_remoney = getRemainmoney(int(this_ormoney), int(this_usemoney))  # 함수 사용하여 남은 금액 작성
    this_cause = cause  # 사용자한테 받은 이유 넣기
    this_hash = last_block.hash


    return Block(this_index, this_timestamp, this_ormoney, this_usemoney, this_remoney, this_cause, this_hash)


#main 시작
if __name__ == "__main__":
    import sys

    #gui 생성
    app = QtWidgets.QApplication(sys.argv)

    # QtWidgets은 UI를 구성해주는 클래스들을 포함하고 있음
    # 해당 소스는 Widget임으로 QtWidgest의 QWidget 메소드 호출
    Form = QtWidgets.QWidget()

    # 위에서 정의한 UI Form을 Form 객체에 적용하고 있음
    ui = Ui_Form()
    ui.setupUi(Form)

    # Widget은 일단 메모리에 적재된 뒤 show 메소드로 화면에 보여짐
    Form.show()

    sys.exit(app.exec_()) 
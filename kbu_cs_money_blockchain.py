#pyqt5를 사용하여 gui사용
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QLineEdit, QPushButton, QTextEdit

#블록체인을 위하여
import hashlib as hasher
import datetime as date

blockchain = []  # 블록이 연결되어 있음
previous_block = []  # 이전의 블록을 저장. 인덱스 번호를 가져와 다음 블록에 1을 더할거임
block_to_add = []  # 연결할 블록


#Ui를 정의하고 있는 클래스
class Ui_Form(QWidget):

    def __init__(self):
        super().__init__()
        self.setupUi()


    def setupUi(self):
        #날짜
        date_lbl = QLabel('날짜', self)
        date_lbl.move(15,10) #좌표 이동
        self.date_textBox = QLineEdit(self)
        self.date_textBox.setGeometry(100, 10, 250, 20)

        # 사용 금액
        use_lbl = QLabel('사용 금액', self)
        use_lbl.move(15, 40)  # 좌표 이동
        self.use_textBox = QLineEdit(self)
        self.use_textBox.setGeometry(100, 40, 250, 20)


        # 사용 이유
        cause_lbl = QLabel('사용 이유', self)
        cause_lbl.move(15, 70)  # 좌표 이동
        self.cause_textBox = QLineEdit(self)
        self.cause_textBox.setGeometry(100, 70, 250, 20)

        #누적 상황 보여주기
        view_lbl = QLabel('현재 상황', self)
        view_lbl.move(15, 100)  # 좌표 이동
        self.view = QTextEdit(self)
        self.view.setOverwriteMode(True)
        self.view.setReadOnly(True)
        self.view.setGeometry(100, 100, 250, 100)

        #버튼
        addBtn = QPushButton('ADD', self)
        addBtn.move(267,230)
        addBtn.clicked.connect(self.add_btn_clicked)


        self.setGeometry(30,30,370,270)
        self.setWindowTitle('컴소 학회비 투명하게')
        self.show()


    #add 클릭하였을 때 일어나는 일
    def add_btn_clicked(self):
        global blockchain
        global previous_block
        global block_to_add

        date = self.date_textBox.text()
        use_money = self.use_textBox.text()
        cause = self.cause_textBox.text()


        if len(blockchain) == 0:#블록의 길이가 0이면
            # 맨 처음 블록 생성 후 체인으로 블록 묶기
            blockchain = [create_genesis_block()]  # 리스트인 blockchanin에 첫번째 값(genesis) 블록 넣음
            previous_block = blockchain[0]  # 위에서 생성된 첫번째 블록 만듬

            if date:
                block_to_add = next_block(previous_block, date, use_money, cause)  # next_block사용하여 블록 생성
                blockchain.append(block_to_add)  # 맨 처음 붙인 블록에 위에 만든 블록 붙임(리스트임)
                previous_block = block_to_add  # 전의 블록은 위에 생성된 블록으로 바꿈

                #저장한 블록 보여주기
                for i in range(len(blockchain)):
                    stri = str(blockchain[i].timestamp)+' '+str(blockchain[i].usemoney)+' '+str(
                        blockchain[i].cause) + ' ' + str(blockchain[i].remoney)
                    self.view.append(stri)

        else:
            if date:
                block_to_add = next_block(previous_block, date, use_money, cause)  # next_block사용하여 블록 생성
                blockchain.append(block_to_add)  # 맨 처음 붙인 블록에 위에 만든 블록 붙임(리스트임)
                previous_block = block_to_add  # 전의 블록은 위에 생성된 블록으로 바꿈

                # 저장한 블록 보여주기
                stri = str(block_to_add.timestamp) + ' ' + str(block_to_add.usemoney) + ' ' + str(
                    block_to_add.cause) + ' ' + str(block_to_add.remoney)
                self.view.append(stri)

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
    return Block(0, date.datetime.now(), 100000, 0, getRemainmoney(100000, 0), '맨 처음 학회비', "0")


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
    app = QApplication(sys.argv)
    pos = Ui_Form()

    sys.exit(app.exec_()) 
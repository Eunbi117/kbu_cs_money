import hashlib as hasher
import datetime as date

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

#남은 금액 반환하는 함수
def getRemainmoney(ormoney, usemoney):
    return ormoney - usemoney

#맨 처음 블록 생성
def create_genesis_block():
    return Block(0, date.datetime.now(), 100000, 0, getRemainmoney(100000,0),'', "0")

#다음 블록 생성
def next_block(last_block, usemoney, cause):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_ormoney = last_block.remoney #전에 남은 금액이 현재 있는 돈이 된다
    this_usemoney = usemoney #사용한 금액을 매개변수로 받아서 저장
    this_remoney = getRemainmoney(this_ormoney, this_usemoney) #함수 사용하여 남은 금액 작성
    this_cause = cause #사용자한테 받은 이유 넣기
    this_hash = last_block.hash
    
    return Block(this_index, this_timestamp, this_ormoney,this_usemoney,this_remoney,this_cause, this_hash)


#맨 처음 블록 생성 후 체인으로 블록 묶기
blockchain = [create_genesis_block()] #리스트인 blockchanin에 첫번째 값(genesis) 블록 넣음
previous_block = blockchain[0] #위에서 생성된 첫번째 블록 만듬

#체인으로 묶기
#while True:
user_usemoney = int(input('사용한 금액: '))
user_cause = input('사용 이유: ')

block_to_add = next_block(previous_block, user_usemoney, user_cause) #next_block사용하여 블록 생성
blockchain.append(block_to_add) #맨 처음 붙인 블록에 위에 만든 블록 붙임(리스트임)
previous_block = block_to_add #전의 블록은 위에 생성된 블록으로 바꿈

print("쓴 돈 : {}".format(block_to_add.usemoney))
print("남은 돈 : {}".format(block_to_add.remoney))
print("사용 이유 : {}".format(block_to_add.cause))
print("Block #{} has been added to the blockchain!".format(block_to_add.index))




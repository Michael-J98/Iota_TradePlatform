#import os
import base64
import threading
import numpy as np
import time
import sys
sys.path.append('./')
from Basic import Node, Public_Com
from iota import ProposedTransaction, Address, TryteString


class Iot(Node.Node):
    def __init__(self):
        super().__init__()
        self.pow_password = []
        self.carbon_password = []
        self.surplus_pow = 100.0  # kw`h
        self.surplus_carbon = 100.0
        self.production_curve = 50000  # kw
        self.consumption_curve = None
        self.time_interval = 10  # 每10s计算一次电量
        self.pub_client = Public_Com.Client()  # 外部发布或订阅信息到指定频道
        self.sub_client = Public_Com.Client(sub=True)  # 外部发布或订阅信息到指定频道
        self.consumer_address = None
        print('iot实例初始化完成')

    def pow_product(self, *args) -> int:
        if isinstance(self.production_curve, int):
            return self.production_curve

        if callable(self.production_curve):
            return self.production_curve(args)

        print('check the type of self.production_curve, it is either\
        int or function, now:{}'.format(type(self.production_curve)))
        return None

    def pow_consume(self, *args) -> int:
        """
        应按照self.time_interval间隔调用该函数，该函数将同时削减剩余电量
        """
        consumption = None
        if self.consumption_curve is None:
            consumption = np.random.randint(10, 3000)

        if callable(self.consumption_curve):
            consumption = self.consumption_curve(args)

        self.surplus_pow -= self.time_interval * consumption / 3600

        if consumption is None:
            print('check the type of self.consumption_curve, it is either\
            None or function, now:{}'.format(type(self.consumption_curve)))
        
        return consumption

    def pow_psw_generation(self, quantity: float) -> bytes:
        psw = base64.b64encode(bytes(str(quantity), 'utf-8'))
        return psw

    def pow_psw_interpret(self, psw: bytes) -> str:
        quantity = base64.b64decode(psw).decode()
        return quantity


def report_production(iot, *args):
    print('开始上传电力生产')
    while True:
        iot.pub_client.publish('I-P', iot.pow_product(args))
        time.sleep(iot.time_interval/5)


def report_surplus_pow(iot, *args):
    print('开始上传电力剩余')
    while True:
        iot.pub_client.publish('I-C', str({'type': 'surplus', 'amount': iot.surplus_pow}))
        time.sleep(iot.time_interval/5)


def producer_handler(message):
    global iot
    assert isinstance(message['channel'], bytes)
    if message['channel'].decode() == 'P-I':
        if eval(message['data'].decode())['type'] == 'psw_request':
            print('收到密码生成请求')

            address = eval(message['data'].decode())['address']
            assert isinstance(address, Address), f'Type:{type(address)}'
            print('买家Iot地址接收成功:{}'.format(address))

            quantity = eval(message['data'].decode())['quantity']
            print(f'购买电量确认{quantity}')

            pow_psw = iot.pow_psw_generation(quantity)
            print('电网连接密码生成')

            transactions = [
                ProposedTransaction(
                    address=address,
                    value=0,
                    message=TryteString.from_bytes(pow_psw),
                )
            ]

            try:
                Node.decorator(iot.send(transactions))
            except:
                print('重新生成协程对象...')
                Node.decorator(iot.send(transactions))
            print('传送电网连接密码成功')

            

if __name__ == "__main__":
    iot = Iot()  # 生产者IoT设备
    iot.sub_client.subscribe('P-I', thread_on=True, handler=producer_handler)
    production_status = threading.Thread(target=report_production, args=(iot,))
    production_status.daemon = True
    production_status.start()

    time.sleep(300)

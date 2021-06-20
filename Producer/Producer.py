import threading
import time
import sys
sys.path.append('./')
from Basic import Node, Public_Com
from iota import Address


class Producer(Node.Node):
    def __init__(self, **kwargs):
        super().__init__()
        self.pow_password = []
        self.carbon_password = []

        self.pow_production = None  # kw, waiting for iot msg
        self.unit_price = 1  # iota/kw`h
        self.trading_strategy = None

        self.time_interval = 10  # 每10s计算一次电量
        self.pub_client = Public_Com.Client()  # 外部发布或订阅信息到指定频道
        self.sub_client = Public_Com.Client(sub=True)  # 外部发布或订阅信息到指定频道

        self.collection_address  =  None
        self.collection_address_generation() # 收款地址

        for key, value in kwargs.items():
            exec('self.{}={}'.format(key, value))
        print('producer实例初始化完成')

    def collection_address_generation(self):
        try:
            add = Node.decorator(self.address_gen())[0]
        except:
            print('重新生成协程对象...')
            add = Node.decorator(self.address_gen())[0]

        self.collection_address = add

        self.set_price()  # 设置电力价格
        msg = {
            'collection_address' : self.collection_address,
            'price' : self.unit_price
        }

        self.pub_client.client.set('P-C', str(msg))
        print(f'公布报价及收款地址：{msg}')


    def set_price(self, *args):
        if self.trading_strategy is not None:
            assert callable(self.trading_strategy)
            self.unit_price = self.trading_strategy(self.pow_production, args)

        else:
            pass  # using default price

first = True
def IP_handler(message):
    global producer, first
    assert isinstance(message['channel'], bytes)
    if message['channel'].decode() == 'I-P':
        producer.pow_production =  eval(message['data'].decode())
        if first:
            print(f'收到发电信息：{producer.pow_production} kw')
            first = False



def collection_respond(producer):
    print('等待接收IOTA...')
    while True:
        try:
            data = Node.decorator(producer.fetch(producer.collection_address))
        except:
            print('重新生成协程对象...')
            data = Node.decorator(producer.fetch(producer.collection_address))

        if data != []:
            iota = eval(data[0])['iota']  # 遗留项，应该直接获取transaction.value
            address = eval(data[0])['address']
            print(f'收到IOTA：{iota}\n收到Address：{address}')
            quantity = float(int(iota/producer.unit_price))
            print(f'交易电力：{quantity}')
            producer.pub_client.publish('P-I',str({'type':'psw_request', 'address':address, 'quantity':quantity}))
            print('向Iot设备请求电网连接密码生成')
            producer.collection_address_generation()
        time.sleep(1)

            

if __name__ == "__main__":
    producer = Producer(timeout = 300)  # 生产者
    producer.sub_client.subscribe('I-P', thread_on=True, handler=IP_handler)  # 订阅Iot设备频道
    collection_rpd = threading.Thread(target=collection_respond, args=(producer,))
    collection_rpd.daemon = True
    collection_rpd.start()

    time.sleep(300)

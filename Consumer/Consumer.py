import threading
import time
import sys
sys.path.append('./')
from Basic import Node, Public_Com
from iota import ProposedTransaction, Address, TryteString


class Consumer(Node.Node):
    def __init__(self, **kwargs):
        super().__init__()
        self.pow_password = []
        self.carbon_password = []

        self.trading_strategy = None

        self.time_interval = 10  # 每10s计算一次电量
        self.pub_client = Public_Com.Client()  # 外部发布或订阅信息到指定频道
        self.sub_client = Public_Com.Client(sub=True)  # 外部发布或订阅信息到指定频道

        self.collection_address  = None  # 收款地址
        self.iot_adddress = None
        self.trading_unit = 100  # IOTA

        self.amount = None  # 剩余电量
        self.on_trading = False

        for key, value in kwargs.items():
            exec('self.{}={}'.format(key, value))
        print('consumer实例初始化完成')

    def choose_producer(self, *args):
        if not self.on_trading:
            print('选择生产者...')
            wait_time = 60
            if self.trading_strategy is not None:
                assert callable(self.trading_strategy)
                self.collection_address = self.trading_strategy(args)

            else:
                while True:
                    try: 
                        print('尝试获取报价...')
                        if wait_time > 0:
                            self.collection_address = eval(self.pub_client.client.get('P-C'))['collection_address']
                        else:
                            break
                    except TypeError:
                        wait_time -= 5
                        time.sleep(5)
                        print('等待报价...')
                    else:
                        print(f'生产者选择完成，地址为{self.collection_address}')
                        self.address_request()
                        break

    def address_request(self):
        wait_time = 60
        while wait_time>0:
            print('向Iot设备请求密码接收地址...')
            sub_num = self.pub_client.publish('C-I',str({'type':'add_request'}))
            if sub_num == 0:
                wait_time -= 5
                time.sleep(5)
                print('.')
            else:
                print('已发送到Iot设备')
                break

def IC_handler(message):
    global consumer
    assert isinstance(message['channel'], bytes)
    if message['channel'].decode() == 'I-C':

        if eval(message['data'].decode())['type'] == 'surplus':
            consumer.amount = eval(message['data'].decode())['amount']
            print(f'收到剩余电量：{consumer.amount} kw`h')

        if eval(message['data'].decode())['type'] == 'add_rtn':
            consumer.iot_address = eval(message['data'].decode())['address']
            print(f'收到Iot设备地址：{consumer.iot_address}')
            print(f'向生产者发起交易...')
            consumer.on_trading = True
            msg = {
                'iota' : consumer.trading_unit,
                'address' : consumer.iot_address
            }

            transactions = [
                ProposedTransaction(
                    address=consumer.collection_address,
                    value=0,  # consumer.trading_unit
                    message=TryteString.from_string(str(msg)),
                )
            ]
            try:
                Node.decorator(consumer.send(transactions))
            except:
                print('重新生成协程对象...')
                Node.decorator(consumer.send(transactions))
            print('交易请求成功')
            consumer.on_trading = False

def auto_trading(consumer):
    while True:
        if consumer.amount is not None and consumer.amount < 50:
            consumer.choose_producer()
            time.sleep(15)
        time.sleep(2)

if __name__ == "__main__":
    consumer = Consumer(timeout = 300)  # 生产者
    consumer.sub_client.subscribe('I-C', thread_on=True, handler=IC_handler)  # 订阅Iot设备频道
    #consumer.choose_producer()

    auto_trade = threading.Thread(target=auto_trading, args=(consumer,))
    #production_status.daemon = True
    auto_trade.daemon = True

    #production_status.start()
    auto_trade.start()
    time.sleep(300)

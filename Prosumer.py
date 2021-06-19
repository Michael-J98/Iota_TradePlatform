from iota import Iota, Seed
import pandas as pd
import numpy as np


class producer:
    #定义基本属性
    ID = ''
    price = 0#销售价格
    quantity = 0#电量
    tag = ''#电力种类，火电,风电,水电,光伏,核电等
    
    def __init__(self, Id, pr, qu, ta):
        self.ID = Id
        self.price = pr
        self.quantity = qu
        self.tag = ta
    
    def initialize_node(self):
        #节点初始化
        print('initialize node complete')
        return
    
    def initialize_trading_strategy(self):
        #初始化交易策略
        price = self.price
        quantity = self.quantity
        def send_to_IoT():
            #发送电量和价格给自己的IoT设备
            return
        send_to_IoT()
        print('trading strategy initialization complete')
        return
    
    def initialize_pub_sub(self):
        #初始化
        def send_to_IoT():
            return
        def send_to_consumer():
            return
        send_to_IoT()
        send_to_consumer()
        print('Pub/Sub initialization complete.')
        return
    
    def subscribe_channel(self):
        #订阅频道
        
        print('subscribe channel complete')
        return
    
    def receive_from_IoT(self):
        data = ''
        return data
        
    def publish_info(self):
        def generate_address():
            #生成交易地址
            # Generate a random seed, or use one you already have (for the devnet)
            print('Generating a random seed...')
            my_seed = Seed.random()
            # my_seed = Seed(b'MYCUSTOMSEED')
            print('My seed is: ' + str(my_seed))
            # Declare an API object
            api = Iota(
                adapter='https://nodes.devnet.iota.org:443',
                seed=my_seed,
                devnet=True,
            )
            print('Generating the first unused address...')
            # Generate the first unused address from the seed
            response = api.get_new_addresses()
            addy = response['addresses'][0]
            print('My new address is: ' + str(addy))
            print('Go to https://faucet.devnet.iota.org/ and enter you address to receive free devnet tokens.')
            return addy
        address = generate_address()
        price = self.price
        quantity = self.quantity
        tag = self.tag
        #将地址，交易量，价格等推送到频道
        return
    
    def receive_from_channel(self):
        return
    
    def receive_from_producer(self):
        return
    
    def select_producer(self):
        return
    
    def receive_from_consumer(self):
        return
    
    def smart_contract(self):
        return
    
    def publish_password(self):
        return
    
    def connect_consumer_IoT(self):
        return


class consumer:
    #定义基本属性
    ID = ''
    quantity = 0#电量
    tag = ''#电力种类，火电,风电,水电,光伏,核电等
    
    def __init__(self, Id, pr, qu, ta):
        self.ID = Id
        self.price = pr
        self.quantity = qu
        self.tag = ta
        
    def connect_to_tangle(self):
        print('connect to tangle complete')
        return
    
    def receive_IoT_password(self):
        password = 'password'
        status = '' # on/off
        print('Password is %s' %password)
        print('Status is %s' %status)
        return
    
    def initialize_node(self):
        #节点初始化
        print('node initialize complete')
        return
    
    def IOTA_funding(self):
        print('IOTA funding')
        return
    
    def initialize_trading_strategy(self):
        print('trading strategy initialization complete')
        return
    
    def subscribe_channel(self):
        print('subscribe channel complet')
        return
    
    def initialize_pub_sub(self):
        #初始化
        def send_to_IoT():
            return
        def send_to_consumer():
            return
        send_to_IoT()
        send_to_consumer()
        print('Pub/Sub initialization complete.')
        return
    
    def receive_from_IoT(self):
        data = ''
        return data
    
    def receive_from_prosumer(self):
        producer_info = ''
        return producer_info
    
    def select_producer(self, producer_info):
        producer_info = producer_info.sort_values(by = ['price', 'quantity'], ascending = [True, False])
        need_quantity = float(self.quantity)
        transaction_info = producer_info.copy()
        producer_amount = producer_info.shape[0]
        transaction_quantity = np.zeros((producer_amount, 1))
        while True:
            for i in range(producer_amount):
                if need_quantity <= 0:
                    break
                else:
                    seller = producer_info.iloc[i]
                    sell_quantity = float(seller['quantity'])
                    trans_quantity = min(need_quantity, sell_quantity)
                    transaction_quantity[i][0] = trans_quantity
                    need_quantity -= trans_quantity
            if need_quantity <= 0:
                break
        transaction_info['transaction quantity'] = transaction_quantity
        return transaction_info
    
    def publish_info(self):
        return
    
    def receive_from_IoT(self):
        return
    
    def transfer_token(self):
        return
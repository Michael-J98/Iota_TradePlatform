#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from iota import Iota, Seed
import pandas as pd


# In[ ]:


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
        return
    
    def initialize_trading_strategy(self):
        #初始化交易策略
        def send_to_IoT():
            #发送电量和价格给自己的IoT设备
            return
        send_to_IoT()
        return
    
    def initialize_pub_sub(self):
        #初始化
        def send_to_IoT():
            return
        def send_to_consumer():
            return
        send_to_IoT()
        send_to_consumer()
        return
    
    def subscribe_channel(self):
        #订阅频道
        return
    
    def receive_from_IoT(self):
        return
        
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


# In[ ]:


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
        
    def conect_to_tangle(self):
        return
    
    def receive_IoT_password(self):
        return
    
    def initialize_node(self):
        #节点初始化
        return
    
    def IOTA_funding(self):
        return
    
    def initialize_trading_strategy(self):
        return
    
    def subscribe_channel(self):
        return
    
    def initialize_pub_sub(self):
        #初始化
        def send_to_IoT():
            return
        def send_to_consumer():
            return
        send_to_IoT()
        send_to_consumer()
        return
    
    def receive_from_IoT(self):
        return
    
    def receive_from_prosumer(self):
        producer_info = ''
        return producer_info
    
    def select_producer(self, producer_info):
        producer_info = producer_info.sort_values(by = ['price', 'quantity'], ascending = [True, False])
        need_quantity = self.quantity
        columns = list(producer_info.columns)
        columns.append('transaction_quantity')
        transaction_info = pd.DataFrame([], columns = columns, index = producer_info.index)
        while True:
            for row in producer_info.iterrows():
                if need_quantity <= 0:
                    break
                else:
                    sell_quantity = row['quantity']
                    transaction_quantity = min[need_quantity, sell_quantity]
                    transaction_info.loc[row[0]]['transaction_quantity'] = transaction_quantity
                    transaction_info.loc[row[0]]['price'] = producer_info[row[0]]['price']
                    transaction_info.loc[row[0]]['address'] = producer_info[row[0]]['address']
                    need_quantity -= transaction_quantity
            if need_quantity <= 0:
                transaction_info.fillna(0)
                break
        return transaction_info
    
    def publish_info(self):
        return
    
    def receive_from_IoT(self):
        return
    
    def transfer_token(self):
        return


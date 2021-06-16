
import base64
import sys
sys.path.append("..")
from Basic import Node


class iot(Node.Node):
    #note:eq表示电量

    #定义功能函数

    #买家iot获取需求电量，卖家iot获取某一时刻发电量
    def electric_quantity(self,eq):
        return eq

    #买家iot生成密码接收地址:继承类


    #卖家iot接收密码生成地址
    def address_receive(self,address_consumer):
        return address_consumer

    #卖家iot生成含有用电量的密码
    def secret_eq_encode(self,trade_eq):
        eq=f'{trade_eq}'
        secret=base64.b64encode(bytes(eq, 'utf-8'))
        return secret

    #买家通过tangle给买家iot发送密码和购电量

    #买家iot解码获得卖家的购电量
    def secret_eq_decode(self,secret):
        eq=base64.b64decode(secret)
        return eq

    #买家的剩余购买电量
    def rest_eq_demand(self,eq_demand,trade_eq):
        return eq_demand-trade_eq







#TEST
consumer=iot()
AD=consumer.address_gen
print(AD)
eq_demand=50
trade_eq=eq_demand-10
print(eq_demand,trade_eq)
secret=consumer.secret_eq_encode(trade_eq)
print(secret)
eq_de=consumer.secret_eq_decode(secret)
print(eq_de)
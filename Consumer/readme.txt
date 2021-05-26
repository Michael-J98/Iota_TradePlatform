可能包含的文件或方法：

1. Consumer.py
Basic.Node.Node子类
功能
    向Grid指定地址发送transaction
        需求信息【定义基本数据结构, basic.Structure.py】
            需要多少能源【方法及对应数据结构,  Quantity_Strategy.py】
            能源购买价格【方法及对应数据结构, Price_Strategy.py】
            反馈消息接收地址
            有效性
                IoT设备hash值（实例的属性）
                电子签名=信息+私钥（实例的属性）


        确认交易信息【定义数据结构,  basic.Structure.py】
            是否确认交易
            待输送能源的IoT设备物理地址
            向Grid付款


    读取Grid反馈信息【定义数据结构, basic.Structure.py】
        匹配信息


输入接口
    Transaction生成方法【basic.Transaction.py】
    各类数据结构
        能源购买量（区间、策略）
        能源购买价格（区间、策略）

    IoT设备当前物理地址【IoT.IoT.py】

输出接口
    向Grid发出各类transaction

2. Price_Strategy.py

3. Quantity_Strategy.py
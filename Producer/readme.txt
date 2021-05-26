可能包含的文件或方法：

1. Producer.py
Basic.Node.Node子类
功能
    向Grid指定地址发送transaction
        需求信息
            提供多少能源【方法及对应数据结构】
            能源出售价格【方法及对应数据结构】
            反馈消息接收地址
            有效性
                IoT设备hash值（实例属性）
                电子签名=信息+私钥（实例属性）


        确认交易信息【定义数据结构】
            是否确认交易
            卖家收款地址


    读取Grid反馈信息【定义数据结构】
        匹配信息
        买家IoT设备物理地址【多个买家的数据结构？】


输入接口
    Transaction生成方法
    获取IoT设备当前物理地址

2. Price_Strategy.py

3. Quantity_Strategy.py
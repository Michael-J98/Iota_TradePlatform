可能包含的文件或方法：

1. Iot.py
Basic.Node.Node子类
｜ 匿名性：通过随机激活，Grid只知道是它的设备，并且绑定了某个账户，但是不知道是谁买的
功能
    模拟设备激活
        与Grid联网，生成设备hash值
        接收设备专属密钥

    模拟能源生产
    模拟能源消耗
        输送给其他设备
        自身耗散
        ｜ 做功使用掉、热耗散

    发送变化速度
    传送能源
    IoT设备hash值生成实时变化物理地址

输入接口
    设备激活方法
    能源变化信号
    能源接收

输出接口
    发送监控能源信息的transaction到Tangle上
    能源发送
    传出设备hash值、密钥

2. Signal_Generation.py

3. Energy_Transfer.py

4. HashToAddress.py
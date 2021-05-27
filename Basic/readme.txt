可能需要包含的文件或方法（不完整）：

1. Activation.py

2. Cipher.py
功能：
    加密数据
    解密数据

3. Node.py

********************************************************
class Node(**kwargs)
所有客户端节点的基础类（异步）
	Parameters:
		· seed - iota.Seed，用户种子, default = None
		· adapter - str, URI string or BaseAdapter instance, default = 'https://nodes.devnet.iota.org:443'
		· devnet - bool, 是否在测试网络上搭建, default = True
		· addresses - List[iota.types.Address], 历史生成Tangle地址, default = []
		· index - int, 种子生成地址的索引，每次生成地址会加一, default = 0
		· sent_tx_hashes - List[iota.transaction.types.TransactionHash], 待发送transaction存放队列, default = []
		· bundles - List[iota.transaction.types.TransactionHash], 历史transaction存放队列, default = []
		· elapsed - int, 验证等待初始时间, default = 0
		· timeout - int, 验证等待时间上限, default = 120
		· polling_interval - int, 验证等待间隔, default = 5
    ========
    seed_gen()
        生成新种子，并替换self.seed

    ========
    async address_gen(count)
        根据种子在index=self.index处生成count个Tangle 地址, 并添加到self.addresses中
        Parameters:
                · count - int, 生成地址个数, default = 1
        Return:
                · adds - List[iot.types.Address], 本次调用生成的地址

    ========
    async send(transactions)
        发送一系列transaction, tail_transaction hash将被存进self.bundles
        从self.elapsed开始, 每隔self.polling_interval验证transactions是否被Tangle确认
        Parameters:
                · transactions - List[iota.transaction.creation.ProposedTransaction], 生成地址个数, default = 1
        Return:
                · state - bool, transaction是否全部被Tangle确认

    ========
    async fetch(address)
        根据地址/哈希值查询transaction
        Parameters:
                · address - iota.types.Address | str, Tangle上地址类或者长度为81的tail_transaction哈希字符串
        Return:
                · state - List[str], 该地址上接收的所有信息, 可能被base64编码

********************************************************
def decorator(coroutine)
一种简单的获得协程函数返回值的方法
    Parameters:
            · coroutine - coroutine object, 用async修饰的def在call时会返回coroutine object
    Return:
            · 不加async修饰的def的返回值

4. Signature.py

5. Structure.py

6. Transaction.py
功能
    编码信息
    加密信息
    创建transaction


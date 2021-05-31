
import time
import hashlib
import rsa

'''
先生成时间戳
grid根据时间戳产生哈希值，并将时间戳发送给iot
iot接收时间戳生成哈希值，将哈希值发送给grid
grid将自己产生的哈希值与接收的哈希值进行比较，TRUE则认证成功
认证成功后，grid生成密钥对，将公钥储存起来，私钥发送给iot
iot接收到私钥后储存起来，连同哈希值发送给prosumer
'''



def time_stamp():
    # 生成13位时间戳
    time_stamp= int(round(time.time() * 1000))
    time_=f"{time_stamp}"
    return time_


def hash_generator(time_stamp):
    #生成哈希值
    md5 = hashlib.md5()
    md5.update(time_stamp.encode(encoding='UTF-8'))
    encryptedSecret = md5.hexdigest()
    return encryptedSecret

def hash_comparation(self_hash,other_hash):
    #比较哈希值
    #if self_hash.equals(other_hash):
    if self_hash == other_hash:
        return True
    else:
        return False


#(pubkey, privkey) = rsa.newkeys(1024)
# 生成公钥、私钥


#函数测试
time_stamp=time_stamp()
print(time_stamp)
hash1=hash_generator(time_stamp)
hash2=hash_generator(time_stamp)
print(hash1,hash2)
if hash_comparation(hash1,hash2):
    (pubkey, privkey) = rsa.newkeys(1024)
    print(pubkey,privkey)
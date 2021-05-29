#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 需要安装rsa库
import rsa


# In[2]:


'''
RSA的加密过程如下：

（1）A生成一对密钥（公钥和私钥），私钥不公开，A自己保留。公钥为公开的，任何人可以获取。

（2）A传递自己的公钥给B，B用A的公钥对消息进行加密。

（3）A接收到B加密的消息，利用A自己的私钥对消息进行解密。

　　在这个过程中，只有2次传递过程，第一次是A传递公钥给B，第二次是B传递加密消息给A，即使都被敌方截获，也没有危险性，因为只有A的私钥才能对消息进行解密，防止了消息内容的泄露。

RSA签名的过程如下：

（1）A生成一对密钥（公钥和私钥），私钥不公开，A自己保留。公钥为公开的，任何人可以获取。

（2）A用自己的私钥对消息加签，形成签名，并将加签的消息和消息本身一起传递给B。

（3）B收到消息后，在获取A的公钥进行验签，如果验签出来的内容与消息本身一致，证明消息是A回复的。

　　在这个过程中，只有2次传递过程，第一次是A传递加签的消息和消息本身给B，第二次是B获取A的公钥，即使都被敌方截获，也没有危险性，因为只有A的私钥才能对消息进行签名，即使知道了消息内容，也无法伪造带签名的回复给B，防止了消息内容的篡改。

但是，综合两个场景你会发现，第一个场景虽然被截获的消息没有泄露，但是可以利用截获的公钥，将假指令进行加密，然后传递给A。第二个场景虽然截获的消息不能被篡改，但是消息的内容可以利用公钥验签来获得，并不能防止泄露。所以在实际应用中，要根据情况使用，也可以同时使用加密和签名，比如A和B都有一套自己的公钥和私钥，当A要给B发送消息时，先用B的公钥对消息加密，再对加密的消息使用A的私钥加签名，达到既不泄露也不被篡改，更能保证消息的安全性。

总结：公钥加密、私钥解密、私钥签名、公钥验签。
'''


# In[3]:


(pubkey, privkey) = rsa.newkeys(1024)
# 生成公钥、私钥


# In[4]:


def rsa_encrypt(str):
    # ras加密
    content = str.encode('utf-8')
    crypto = rsa.encrypt(content, pubkey)
    return crypto


# In[5]:


def rsa_decrypt(content, key):
    # rsa解密，私钥
    content = rsa.decrypt(content, key).decode('utf-8')
    return content


# In[6]:


def rsa_sign(crypto, privkey):
    # rsa签名
    return rsa.sign(crypto, privkey, 'SHA-256')


# In[15]:


def rsa_verify(content, sign_content, pubkey):
    # 验证签名，返回T/F
    try:
        result = rsa.verify(content, sign_content, pubkey)
    except:
        return False
    else:
        return True


# In[8]:


message = 'hello world' # 原文
crypto = rsa_encrypt(message) # 公钥加密内容


# In[16]:


sign_content = rsa_sign(crypto, privkey) # 私钥签名公钥加密之后的内容


# In[20]:


wrong_crypto = rsa_encrypt(message + message)


# In[18]:


# 签名验证为真的例子
print(rsa_verify(crypto, sign_content, pubkey)) # 公钥验签


# In[21]:


# 签名验证失败的例子
print(rsa_verify(wrong_crypto, sign_content, pubkey))


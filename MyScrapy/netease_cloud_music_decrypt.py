import base64
import binascii
import codecs
import json
import random
# 需要安装 pycryptodemo
from Crypto.Cipher import AES


class NeteaseCloudMusicDecrypt():
    """网易云音乐爬虫解密类"""

    def __init__(self, song_id, offset, limit, total):
        self.page_param = {
            'rid': "R_SO_4_" + song_id,
            'offset': offset,
            'limit': limit,
            'total': total,
            'csrf_token': ""
        }
        self.pub_key = '010001'
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5a' \
                           'a76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7' \
                           'a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.secret_key = b'0CoJUm6Qyw8W8jud'
        self.random_str = self.create_random_16()

    def create_random_16(self):
        """获取随机16个字母拼接的字符串"""
        return bytes(''.join(random.sample('1234567890DeepDarkFantasy', 16)), 'utf-8')

    def aes_encrypt(self, text, key):
        """aes加密"""
        # 对长度不是16倍数的字符串进行补全，然后再转为bytes数据
        pad = 16 - len(text) % 16
        try:
            # 如果接到bytes数据（如第一次aes加密得到的密文）要解码再进行补全
            text = text.decode()
        except:
            pass
        text = text + pad * chr(pad)
        try:
            text = text.encode()
        except:
            pass
        encryptor = AES.new(key, AES.MODE_CBC, b'0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)  # 得到的密文还要进行base64编码
        return ciphertext

    def rsa_encrypt(self, pub_key, text, modulus):
        """rsa加密"""
        text = text[::-1]  # 明文处理，反序并hex编码
        rsa = int(binascii.hexlify(text), 16) ** int(pub_key, 16) % int(modulus, 16)
        return format(rsa, 'x').zfill(256)

    def get_param(self):
        """获取param"""
        # print(self.random_str)
        # print(self.page_param)
        # print(type(self.page_param))
        text = json.dumps(self.page_param)
        params = self.aes_encrypt(text, self.secret_key)
        params = self.aes_encrypt(params, self.random_str)
        # params = self.aes_encrypt(self.aes_encrypt(text, nonce), key)
        return params

    def get_encSecKey(self):
        """获取encSEcKey"""
        text = self.random_str
        pub_key = self.pub_key
        modulus = self.modulus
        encSecKey = self.rsa_encrypt(pub_key, text, modulus)
        return encSecKey


# def main():
#     decrypt = NeteaseCloudMusicDecrypt('513360721', '2', '20', 'false')
#     params = decrypt.get_param()
#     encSecKey = decrypt.get_encSecKey()
#     return {'params': params.decode(),
#      'encSecKey': encSecKey}
#
#
# main()


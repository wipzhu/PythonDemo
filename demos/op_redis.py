import redis
from redis import Redis

if __name__ == '__main__':
    redisCli = Redis(host='192.168.56.56',
                     port=6379, db=0)

    redisCli.set('wipzhu', 'itheima')

    redisCli.hset('mingzi:test', "chineseName", '朱小花')
    redisCli.hset('mingzi:test', "englishName", 'wipzhu')

    a1 = redisCli.get('wipzhu')
    print(a1)

    a2 = redisCli.hmget('mingzi:test', ['chineseName', 'englishName'])
    print(a2)


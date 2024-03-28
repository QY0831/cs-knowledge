# REST API:
# 缩短URL:
# POST api/v1/data/shorten
# 重定向URL:
# GET api/v1/shortUrl
import string

BASE62_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase
# 设tiny url长度为N, 则支持62^N个地址

"""       
输入：长URL --> 长URL在数据库中 ---否--> 生成一个新ID --> 把ID转化为短URL --> 将ID、短URL、长URL保存到数据库
                    |                      
                    |                      
                    +-----------是---->返回短URL               
"""
class TinyURL:
    def __init__(self):
        self.url_to_id = {}
        self.id_to_url = {}
        self.current_id = 0

    def encode(self, long_url):
        if long_url in self.url_to_id:
            return self.convert_to_base62(self.url_to_id[long_url])

        short_url = self.convert_to_base62(self.current_id)
        self.url_to_id[long_url] = self.current_id
        self.id_to_url[self.current_id] = long_url
        self.current_id += 1

        return short_url

    def decode(self, short_url):
        id = self.convert_from_base62(short_url)
        return self.id_to_url.get(id)

    def convert_to_base62(self, num):
        if num == 0:
            return BASE62_CHARS[0]

        base62 = ''
        while num > 0:
            num, remainder = divmod(num, 62) # 不断对62取模，得到对应的字符
            base62 = BASE62_CHARS[remainder] + base62

        return base62

    def convert_from_base62(self, base62):
        num = 0
        for char in base62:
            num = num * 62 + BASE62_CHARS.index(char)

        return num

# 示例用法
tiny_url = TinyURL()
long_url = "https://www.example.com/long-url"
short_url = tiny_url.encode(long_url)
print("Short URL:", short_url)
decoded_url = tiny_url.decode(short_url)
print("Decoded URL:", decoded_url)

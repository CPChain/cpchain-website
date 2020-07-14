"""

根据 IP 地址获取其地理位置，通过接口实现

1. 淘宝的API（推荐）：http://ip.taobao.com/service/getIpInfo.php?ip=110.84.0.129
2. 国外freegeoip.net（推荐）：http://freegeoip.net/json/110.84.0.129 这个还提供了经纬度信息（但不一定准）
3. 新浪的API：http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=110.84.0.129
4. 腾讯的网页查询(返回的非json格式): http://ip.qq.com/cgi-bin/searchip?searchip1=110.84.0.129
5. ip.cn的网页（返回的非json格式）：http://www.ip.cn/index.php?ip=110.84.0.129
6. ip-api.com： http://ip-api.com/json/110.84.0.129

pytest -v -s tests

"""
import requests

def test_get_geo_for_ip():
    print()
    resp = requests.get(url = 'http://ip-api.com/json/%s' % ('3.115.236.139'))
    data = resp.json()
    print(data)


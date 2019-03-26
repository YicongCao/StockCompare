# coding=utf-8
import requests
import json

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0'
}
RTX_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={0}"
REPLACE_STR = "min_data_{0}{1}="
STOCK_URL = "http://web.ifzq.gtimg.cn/appstock/app/{0}Minute/query?_var=min_data_{0}{1}&code={0}{1}"
USD_TO_HKD = "https://hq.sinajs.cn/?list=fx_susdhkd,fx_susdhkd_i"


def get_html_from_url(url):
    if None == url:
        print("url is None")
        return None
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print("open {0} failed".format(url))
        return None
    return r.text


def push_to_im(bot_id, md_msg):
    url = RTX_WEBHOOK_URL.format(bot_id)
    json = {
        "msgtype": "markdown",
        "markdown": {
            "content": md_msg
        }
    }
    print("pushing bot: ", bot_id)
    r = requests.post(url, json=json)
    print("pushing result:\r\n", r.text, "\r\n")
    print("pushing details:\r\n", r.status_code, " ", r.reason, "\r\n")


def get_market_value_of_stock(market, stock, detailed=False):
    if 'us' != market and 'hk' != market:
        print("market not supported: ", market)
        return None
    if None == stock:
        print("stock is None")
        return None
    url = STOCK_URL.format(market, stock)
    rep = REPLACE_STR.format(market, stock)
    html = get_html_from_url(url)
    html = str(html).replace(rep, "")
    stock_json = json.loads(html)
    sel = "{0}{1}".format(market, stock)
    market_val = stock_json["data"][sel]["qt"][sel][45]
    print(stock, "'s market value is ", market_val)
    if detailed:
        return {
            "market_value": float(market_val),
            "name": stock_json["data"][sel]["qt"][sel][1],
            "price": stock_json["data"][sel]["qt"][sel][3],
            "chg_per": stock_json["data"][sel]["qt"][sel][32],
            "market": market,
            "symbol": stock
        }
    else:
        return float(market_val)


def get_usd_to_hkd():
    html = get_html_from_url(USD_TO_HKD)
    fx_str = str(html).split(";")[0].replace(
        "var hq_str_fx_susdhkd=", "").split(",")
    # print(fx_str)
    print("1 usd = {0} hkd".format(fx_str[1]))
    return float(fx_str[1])


def compare_two_stocks(stock_a, stock_b):
    # A股票今天超过B股票了吗？
    stock_a = get_market_value_of_stock(
        stock_a["market"], stock_a["symbol"], detailed=True)
    stock_b = get_market_value_of_stock(
        stock_b["market"], stock_b["symbol"], detailed=True)
    val_a = stock_a["market_value"]
    val_b = stock_b["market_value"]
    # hkd to usd
    usd_to_hkd = get_usd_to_hkd()
    if 'hk' == stock_a["market"]:
        val_a = val_a / usd_to_hkd
        stock_a["market_value"] = val_a
    if 'hk' == stock_b["market"]:
        val_b = val_b / usd_to_hkd
        stock_b["market_value"] = val_b
    if val_a >= val_b:
        answer = '### **<font color="red">是的！</font>**'
        desc = "今晚**继续加班**才能保持第一呢～"
    else:
        answer = '### **<font color="info">没有…</font>**'
        desc = "你看我们市值都落后阿里了，今晚就**加加班**吧"
    # details
    details = []
    stocks = [stock_a, stock_b]
    for stock in stocks:
        if '-' in stock["chg_per"]:
            chg = '<font color="info">' + \
                stock["chg_per"] + '%</font>'
        else:
            chg = '<font color="red">' + \
                stock["chg_per"] + '%</font>'
        if 'us' == stock["market"]:
            price = str(round(float(stock["price"]), 2)) + "美元"
        elif 'hk' == stock["market"]:
            price = str(round(float(stock["price"]), 2)) + "港币"
        else:
            price = stock["price"]
        details.append("> **{0}**: 市值 {1}亿美元, 股价 {2}, 变动 {3}".format(
            stock["name"],
            round(stock["market_value"], 2),
            price,
            chg))
    # generate md
    paras = [answer, desc, "\r\n".join(details)]
    md = "\r\n\r\n".join(paras)
    print("\r\ngenerate md:\r\n", md, "\r\n")
    return md


if __name__ == "__main__":
    market_val = get_market_value_of_stock("hk", "00700")
    market_val = get_market_value_of_stock("us", "BABA.N")
    get_usd_to_hkd()

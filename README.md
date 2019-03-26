## 今天腾讯市值超过阿里了吗？

- 功能：股票市值比较脚本，可设置定时推送。支持美股和港股的换算。
- 数据源：腾讯财经（股价）、新浪财经（汇率）

![企业微信Bot推送](https://ws3.sinaimg.cn/large/006tKfTcgy1g1gazk7eafj30gh0bwq4e.jpg)

- 配置：编辑 `config.json` 可以改成其他股票：

```json
{
    "last_update": 0,
    "watch_list": [{
        "remark": "今天腾讯股价超过阿里了吗",
        "bot_id": "12312392-2c14-4f2f-8786-2ea7b3123123",
        "stocks": [{
                "symbol": "00700",
                "market": "hk",
                "remark": "腾讯"
            },
            {
                "symbol": "BABA.N",
                "market": "us",
                "remark": "阿里"
            }
        ]
    }]
}
```


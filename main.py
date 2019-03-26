# coding=utf-8
import os
import json
import time
import sys

import utils
# 防止秒表不准产生偏差，隔天运行检查23h即可
ONE_DAY = 24 * 60 * 60
ONE_HOUR = 60 * 60
LESS_THAN_ONE_DAY = ONE_DAY - ONE_HOUR
CONFIG_FILE = "config.json"

if __name__ == "__main__":
    with open(CONFIG_FILE, 'r+', encoding='utf-8') as f:
        cfg_text = f.read()
        print("reading config\r\n", cfg_text, "\r\n")
        cfg_json = json.loads(cfg_text)
        # 一天活动一次
        cur_time = time.time()
        last_time = int(cfg_json['last_update'])
        if cur_time - last_time > LESS_THAN_ONE_DAY:
            print('one day passes since last update')
            # 启动更新逻辑
            for watch_item in cfg_json['watch_list']:
                print('updating: ', watch_item['remark'])
                print('bod_id: ', watch_item['bot_id'])
                md = utils.compare_two_stocks(
                    watch_item['stocks'][0], watch_item['stocks'][1])
                utils.push_to_im(watch_item['bot_id'], md)
            # 回写更新时间
            cfg_json['last_update'] = int(time.time())
            cfg_text = json.dumps(cfg_json, indent=4, ensure_ascii=False)
            f.seek(0)
            f.write(cfg_text)
            f.truncate()
        else:
            print('just updated today, quitting...')
            sys.exit(0)

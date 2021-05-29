import json
import os
import sys
import time

import requests

folder = "wallets"  # .json
page_num_path = folder + "/page_num.txt"
_timeout = 20
time_gap = 5
count_quick_response = 0
count_success_time = 0

# 对url中的钱包名称，创建 path/<wallet_name>.txt，如果已存在该文件，则先读取
# 每一行 {"found":true,"label":"HelixMixer-old16","wallet_id":"0004112fc95eace0",
# "addresses_count":10357,"addresses":[
# {"address":"16nUL22Ze63gYBnWu8bhKkTDhreWa5ZihW","balance":0,"incoming_txs":10,
# "last_used_in_block":418150},
# ],
# "updated_to_block":683309}
# 如果存在path/<wallet_name>.end，则证明已获取完成
def thread(wallet_name):
    global _timeout, count_quick_response, time_gap, count_success_time
    url = "<to be fill>" + wallet_name + "<to be fill>"

    print("Gettting: " + wallet_name)
    try_times = 5
    while try_times > 0:
        try_times -= 1
        try:
            print("Timeout:" + str(_timeout) + "\tTime Gap:" + str(time_gap))
            r = requests.get(url, timeout=_timeout).text
        except :
            print(sys.exc_info())
            time_gap += 2
            time.sleep(time_gap)
            continue
        try:
            r_js = json.loads(r)
            break
        except :
            # "Too many requests"
            print(sys.exc_info())
            print(r)
            time_gap += 2
            time.sleep(time_gap)
            continue

    count_success_time += 1
    if count_success_time > 5:
        if time_gap > 2:
            time_gap -= 1
        count_success_time = 0


    print("Get")

    all_addr = r_js["addresses_count"]
    with open(page_num_path, "a") as f:
        f.write(json.dumps({wallet_name: all_addr}) + "\n")

    time.sleep(time_gap)

def main():
    if not os.path.isfile("running36"):
        with open("running36", "w") as __f:
            pass
    service_to_urls = {}
    for name in os.listdir(folder):
        if name.endswith(".json"):
            print(name)
            with open(folder + "/" + name) as wallet_f:
                service_to_urls.update(json.loads(wallet_f.read()))
    print(len(service_to_urls))
    # 读取已获取的
    wallet_name_set = set()
    if os.path.isfile(page_num_path):
        with open(page_num_path) as f:
            while True:
                _l = f.readline()
                if _l == "":
                    break
                wallet_name_set.update(json.loads(_l).keys())

    for service in service_to_urls:
        for url in service_to_urls[service]:
            if url[url.rindex("/") + 1:] in wallet_name_set:
                continue
            thread(url[url.rindex("/") + 1:])
            if not os.path.isfile("running36"):
                exit(0)


if __name__ == '__main__':
    main()
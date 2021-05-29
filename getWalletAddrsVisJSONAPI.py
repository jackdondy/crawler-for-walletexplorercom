import json
import os
import sys
import time

import requests

folder = "wallets"  # .json
addr_folder = folder + "/addrs"

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
def thread(src_url, path):
    global _timeout, count_quick_response, time_gap, count_success_time
    wallet_name = src_url[src_url.rindex("/") + 1:]
    if os.path.isfile(path + "/" + wallet_name + ".end"):
        return
    wallet_path = path + "/" + wallet_name + ".txt"
    print(wallet_path)
    count_addr = 0
    all_addr = 0

    if os.path.isfile(wallet_path):
        # 读取已获取的
        with open(wallet_path) as f:
            while True:
                _l = f.readline().replace("\n", "")
                if _l == "":
                    break
                count_addr += 100
                if all_addr == 0:
                    all_addr = json.loads(_l)["addresses_count"]

    with open(wallet_path, "a") as f:
        while True:
            if 0 < all_addr <= count_addr:
                with open(path + "/" + wallet_name + ".end", "w") as __f:
                    pass
                return

            url = "<to be filled>" + wallet_name + "&from=" + str(count_addr) + "&count=100&caller=<to be filled>"

            print("Gettting: " + wallet_name + "\t" + str(count_addr))
            try_times = 5
            while try_times > 0:
                try:
                    start_time = time.time()
                    print("Timeout:" + str(_timeout) + "\tTime Gap:" + str(time_gap))
                    r = requests.get(url, timeout=_timeout).text
                    break
                except :
                    print(sys.exc_info())
                    print(r)
                    count_quick_response = 0
                    try_times -= 1
                    time_gap += 2
                    continue

            if try_times <= 0:
                return  # 不成功，放弃继续获取该service及文件

            try:
                r_js = json.loads(r)
            except :
                # "Too many requests"
                print(sys.exc_info())
                print(r)
                _timeout += 5
                count_quick_response = 0
                time_gap += 2
                continue

            count_success_time += 1
            if count_success_time > 5:
                if time_gap > 2:
                    time_gap -= 1
                count_success_time = 0

            if time.time() - start_time < _timeout - 5:
                count_quick_response += 1
            if count_quick_response > 5:
                _timeout -= 5
                if _timeout < 20:
                    _timeout = 20
                count_quick_response = 0

            print("Get")
            f.write(json.dumps(r_js) + "\n")

            if all_addr == 0:
                all_addr = r_js["addresses_count"]

            count_addr += 100

            time.sleep(time_gap)

def main():
    service_to_urls = {}
    for name in os.listdir(folder):
        if name.endswith(".json"):
            print(name)
            with open(folder + "/" + name) as wallet_f:
                service_to_urls.update(json.loads(wallet_f.read()))
    print(len(service_to_urls))
    for service in service_to_urls:
        path = addr_folder + "/" + service
        if not os.path.isdir(path):
            os.mkdir(path)
        for url in service_to_urls[service]:
            thread(url, path)

if __name__ == '__main__':
    main()
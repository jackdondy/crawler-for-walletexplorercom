import json

import requests
from bs4 import BeautifulSoup



header = {"Content-Type": "application", 'Connection': 'close',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

folder = "wallets"

if __name__ == '__main__':
    url = "https://www.walletexplorer.com"
    html = requests.get(url, timeout=5, headers=header).text
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())
    s1 = soup.find(attrs={'class': 'serviceslist'})
    # s1 = s1.contents
    s1 = s1.tr

    for services in s1.children:
        # print(services.prettify())
        service_type = services.h3.string.replace(":", "").replace("/", "or")
        print(service_type)
        with open(folder + "/" + service_type + ".json", "w") as f:
            service_to_url = {}
            for service in services.ul.children:
                service_name = ""
                for url_tag in service.find_all('a'):
                    if service_name == "":
                        service_name = url_tag.string
                        service_to_url[service_name] = []
                    service_to_url[service_name].append(url + url_tag.get('href'))
                print(service_to_url[service_name])
            f.write(json.dumps(service_to_url))

    # print(s1.prettify())
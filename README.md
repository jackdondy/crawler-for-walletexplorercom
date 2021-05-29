# crawler-for-walletexplorercom
this is a crawler for the website [walletexplorer](https://www.walletexplorer.com)
## [getWalletsFromWalletExplorer.py](getWalletsFromWalletExplorer.py)
Use BeautifulSoup to crawl the wallets on [https://www.walletexplorer.com](https://www.walletexplorer.com/) & Write the name and urls of wallets in .json files under [wallets](wallets) directory.
## [getTotalAddrNumViaJSONAPI.py](getTotalAddrNumViaJSONAPI.py)
Use Multi-Thread to get the address-numbers of wallets & write them to [wallets/page_num.txt](wallets/page_num.txt).
To use [this program](getTotalAddrNumViaJSONAPI.py), please contact the owner of [walletexplorer](https://www.walletexplorer.com/) via email ales.janda@kyblsoft.cz for a JSON API, and fill the line 17 of [getTotalAddrNumViaJSONAPI.py](getTotalAddrNumViaJSONAPI.py).
## [getWalletAddrsVisJSONAPI.py](getWalletAddrsVisJSONAPI.py)
Use Multi-Thread to get the addresses of wallets & write them to folders under [wallets/addrs](wallets/addrs) directory. Use wallet name as folder name.
Crawl the addresses of all wallets will take more than a month. 
To use [this program](getWalletAddrsVisJSONAPI.py), please contact the owner of [walletexplorer](https://www.walletexplorer.com/) via email ales.janda@kyblsoft.cz for a JSON API, and fill the line 52 of [getWalletAddrsVisJSONAPI.py](getWalletAddrsVisJSONAPI.py).

## .json files under [wallets](wallets)
Build time: 2021-5-12
## [wallets/page_num.txt](wallets/page_num.txt)
Build time: 2021-5-15
## the zip files under [temp](temp)
Time: 2021-5-13 to 2021-5-22.
In the zip are two folders, corresponding to two wallets, but each of it doesn't contain all the addresses of the wallet.

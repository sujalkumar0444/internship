# Description: This script checks the validity of a list of proxies and returns the valid ones.
import requests

def test_proxy(proxy):
    try:
        response = requests.get("https://x.com", proxies={"http": proxy, "https": proxy}, timeout=10)
        return response.status_code == 200
    except:
        return False

def get_valid_proxies(proxy_list):
    valid_proxies = []
    for proxy in proxy_list:
        if test_proxy(proxy):
            valid_proxies.append(proxy)
            print(proxy)
        else:
            print("failed")    
    return valid_proxies

with open("proxylist.txt", 'r') as f:
    proxies = f.read().split("\n")

valid_proxies = get_valid_proxies(proxies)
print(valid_proxies)

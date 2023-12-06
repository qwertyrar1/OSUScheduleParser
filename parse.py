from bs4 import BeautifulSoup
import requests


def parser(url, day):
    headers = {
        "Accept": "*/*",
        "User-Agent": "user agent"
    }
    req = requests.get(url, headers=headers).text
    soup = BeautifulSoup(req, 'lxml')
    all_tr = soup.findAll('tr')
    check = 0
    for i in range(len(all_tr)):
        if all_tr[i] == soup.select('tr[style="background:#dfd;font-weight:bold"]')[0]:
            check = 1
        if check == 0:
            all_tr[i] = 0
    all_tr = [i for i in all_tr if i != 0]
    all_tr = [i for i in all_tr if i.contents[0].text[:7] != 'Общефиз']
    all_tr = [i for i in all_tr if i.contents[0].text[:5] != 'Ин.яз']
    all_tr = [i for i in all_tr if i.contents[0].text != ' ']
    for this_day in range(len(all_tr)):
        if this_day == day - 1:
            return [j.text for j in all_tr[this_day].findAll('td')]


def parser_all_day(url):
    headers = {
        "Accept": "*/*",
        "User-Agent": "user agent"
    }
    req = requests.get(url, headers=headers).text
    soup = BeautifulSoup(req, 'lxml')
    all_tr = soup.findAll('tr')
    check = 0
    for i in range(len(all_tr)):
        if all_tr[i] == soup.select('tr[style="background:#dfd;font-weight:bold"]')[0]:
            check = 1
        if check == 0:
            all_tr[i] = 0
    all_tr = [i for i in all_tr if i != 0]
    all_tr = [i for i in all_tr if i.contents[0].text[:7] != 'Общефиз']
    all_tr = [i for i in all_tr if i.contents[0].text[:5] != 'Ин.яз']
    all_tr = [i for i in all_tr if i.contents[0].text != ' ']
    for day in range(len(all_tr) - 1):
        yield [j.text for j in all_tr[day].findAll('td')]

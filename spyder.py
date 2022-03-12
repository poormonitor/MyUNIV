from bs4 import BeautifulSoup
import requests

root = "http://zt.zjzs.net/xk2020/"
response = requests.get(root + "allcollege.html")
response.encoding = "utf-8"
bs = BeautifulSoup(response.text, "html.parser")
tab = list(bs.find("table").find_all("tr"))[2:]
for i in tab:
    item = list(i.find_all("td"))
    province = item[0].text
    code = int(item[1].text)
    name = item[2].text
    url = item[3].a.attrs["href"]
    next_url = root + "%d.html" % code
    rs = requests.get(next_url)
    rs.encoding = "utf-8"
    bst = BeautifulSoup(rs.text, "html.parser")
    tab = list(bst.find("table").find_all("tr"))
    for j in tab:
        item = list(j.find_all("td"))
        if not item:
            continue
        major = item[1].text
        must = item[2].text
        print(major,must)
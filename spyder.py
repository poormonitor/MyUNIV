from bs4 import BeautifulSoup
import pandas
import requests
from tqdm import tqdm

df = pandas.DataFrame(columns=["省份", "院校名称", "专业（类）名称", "类中所含专业", "层次", "选考科目要求"])

root = "http://zt.zjzs.net/xk2020/"
response = requests.get(root + "allcollege.html")
response.encoding = "utf-8"
bs = BeautifulSoup(response.text, "html5lib")
tab = list(bs.find("table").find_all("tr"))[2:]
last = "北京"
for i in tqdm(tab):
    try:
        item = list(i.find_all("td"))
        province = item[0].text
        code = int(item[1].text)
        name = item[2].text
        url = item[3].a.attrs["href"]
        next_url = root + "%d.html" % code
        rs = requests.get(next_url)
        rs.encoding = "utf-8"
        bst = BeautifulSoup(rs.text, "html5lib")
        tab = bst.find("table").find_all("tr")
        for j in tab:
            item = list(j.find_all("td"))
            if not item:
                continue
            major = item[1].text
            must = item[2].text
            level = item[0].text
            include = "、".join(list(item[3].strings))
            new = pandas.DataFrame(
                [[province, name, major, include, level, must]],
                columns=["省份", "院校名称", "专业（类）名称", "类中所含专业", "层次", "选考科目要求"],
            )
            df = pandas.concat([df, new])
        if province != last:
            print("%s %d" % (last, len(df)))
            last = province
    except KeyboardInterrupt:
        break
    except IndexError:
        pass
    except:
        raise
df.to_excel("data.xlsx", index=False)

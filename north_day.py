from tkinter.tix import InputOnly
import requests
import pandas as pd
import time
import datetime
 
def download_history_data(name, url=None):
    date_str = datetime.datetime.now().strftime("%y-%m-%d")

    if url == None:
        url="http://data.10jqka.com.cn/hgt/hgtb/"
    else:
        pass

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    data = response.text
    data_list = data.split("\t")
    choose_list = [x for x in data_list if x.startswith("var dataDay")]
    day_data = choose_list[0].split(";")[0].split("var dataDay = ")[1]
    aa = eval(day_data)
    df = pd.DataFrame(aa[0])
    df.rename(columns={0:"time", 1:"flow_in",2: "remain"}, inplace=True)
    df.to_csv(date_str + "." + name + ".tsv", sep="\t", index=False)


 
if __name__ == '__main__':
    download_history_data("sh")
    download_history_data("sz", url="http://data.10jqka.com.cn/hgt/sgtb/")
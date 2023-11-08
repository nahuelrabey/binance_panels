import typing as typ
import plot
import matplotlib.pyplot as plt
import traceback
import ideal_markets as ideal
import time
from main import get_tickers
from win11toast import toast

tickers = get_tickers()

type Ticks = list[int]
type Tickers = list[int]
type CheckerCallable = typ.Callable[[Tickers, str,Ticks],list[ideal.TickerDataTouple]]
type Checker = typ.Callable[[int, Ticks], list[str]]

def check_1s(ticks:list[int]):
    try:
        res = ideal.by_crossing_emas(tickers, "1s", ticks)
    except:
        print(traceback.format_exc())
        return []

    if (len(res)==0):
        return []
    
    return res

def check_1m(ticks:list[int]):
    try:
        res = ideal.by_crossing_emas(tickers, "1m", ticks)
    except:
        print(traceback.format_exc())
        return []

    if (len(res)==0):
        return []
    
    
    return res
def check_15m(ticks:list[int]):
    try:
        res = ideal.by_crossing_emas(tickers, "15m", ticks)
    except:
        print(traceback.format_exc())
        return [] 

    if (len(res)==0):
        return []
    
    return res
    # tickers_names = []
    # for name, _ in res:
    #     tickers_names.append(name)
    
    # return tickers_names 

def check_1h(ticks: list[int]):
    try:
        res = ideal.by_crossing_emas(tickers, "1h", ticks)
    except:
        print(traceback.format_exc())
        return []

    if (len(res)==0):
        return []
    
    return res

def create_links(tickers:list[str]):
    res = []
    for t in tickers:
        res.append(f"<a href='https://www.binance.com/en/trade/{t}' target='_blank'>{t}</a>")
    return res

def create_console_message(info:list[dict]):
    res = ""
    # tickers = unzip_tickers_names(info["tickers"])
    for time in info:
        res += time["title"] + "\n"
        tickers = unzip_tickers_names(time["tickers"])
        res += " ".join(tickers)+"\n"
    return res

def create_html_message(info:list[dict]):
    res = "<div>\n"
    for time in info:
        title = f"<h4>{time['title']}</h4>\n" 
        tickers = unzip_tickers_names(time["tickers"])
        links = "<p>"+"\n".join(create_links(tickers))+"</p>\n"
        res += title
        res += links
    res += "</div>"
    return res

def unzip_tickers_names(seq: list[ideal.TickerDataTouple]):
    res: list[str] = []
    for name, _ in seq:
        res.append(name)
    return res

def save_images(seq: list[ideal.TickerDataTouple], ticks:list[int], id:str):
    for name, data in seq:
        file_name = f"imgs/{name}_{id}.png"
        plot.plot_emas(data, ticks, path=file_name) 

        # plt.savefig(f"{name}_{id}.png")
    

if __name__ == "__main__":
    while True:
        print("running")
        ticks = [10,40,100]

        # 30 minutos, 1hora y 2horas
        # t1s_ticks = [10, 40, 100]
        t1s_ticks = ticks
        t1s = {
            "title": "Hot crypto in 1s!",
            "tickers": check_1s(t1s_ticks)
        }
        save_images(t1s["tickers"], t1s_ticks, "t1s")

        # 1 hora, 6 horas y 12 horas
        # t1m_ticks =[10, 40, 100] 
        t1m_ticks = ticks
        t1m = {
            "title": "Hot crypto in 1m!",
            "tickers": check_1m(t1m_ticks)
        }
        save_images(t1m["tickers"], t1m_ticks, "t1m")

        # 1 hora, 12 horas y 24 horas
        # t15m_ticks =[10, 40, 100]
        t15m_ticks = ticks
        t15m = {
            "title": "Hot crypto in 15m!",
            "tickers": check_15m(t15m_ticks)
        }
        save_images(t15m["tickers"], t15m_ticks, "t15m")

        # 6 horas, 1 día y 2 días
        # t1h_ticks =[10, 40, 100]
        t1h_ticks = ticks
        t1h = {
            "title": "Hot crypto in 1h!",
            "tickers": check_1h(t1h_ticks)
        }
        save_images(t1h["tickers"], t1h_ticks, "t1h")
        
        times = [t1s, t1m, t15m, t1h]
        console_msg = create_console_message(times)
        html_msg = create_html_message(times)
        with open("./view.html", "w") as file:
            file.write(html_msg)
        toast(console_msg, duration="long")
        time.sleep(30)



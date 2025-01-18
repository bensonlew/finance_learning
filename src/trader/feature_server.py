from math import e
from multiprocessing import Process, Queue
import time
from datetime import datetime

from more_itertools import last
from src.data.update_etf_latest import get_multi_last_price


# 计算两个时间的差
def time_diff(time1, time2):
    # time1 = datetime.strptime(time1, "%H:%M").time()
    # time2 = datetime.strptime(time2, "%H:%M").time()
    datetime1 = datetime.combine(datetime.today(), time1)
    datetime2 = time2

    time_diff = datetime1 - datetime2

    if datetime2:
        return time_diff.seconds
    else:
        return 9999
    

def check_if_in_trade_time(now):
    if (now >= datetime.strptime("09:30", "%H:%M").time() and 
        now <= datetime.strptime("11:30", "%H:%M").time()) or \
        (now >= datetime.strptime("13:00", "%H:%M").time() and 
        now <= datetime.strptime("15:00", "%H:%M").time()):
        return True
    else:
        return False



# 获取实时价格的函数
def get_price(queue):
    # 监控程序实时获取价格, 毎5分钟获取一次
    while True:
        time.sleep(5)
        now = datetime.now().time()
        last_data = None
        last_tick = None
        
        # print(f"[Process 1] Fetching data at {datetime.now()}: {queue.get()}")
        if check_if_in_trade_time(now):
            if time_diff(now, last_tick) < 300: 
                continue
            else:
                data = get_multi_last_price(queue)
                last_tick = data.index[-1]
                if data != last_data:
                    last_data = data
                    queue.put(data)  # 将字典放入队列

# 计算特征的函数
def calculate_features(queue_in, queue_out):


    data = queue_in.get()  # 等待进程 1 的字典
    print(f"[Process 2] Received data at {datetime.now()}: {data}")
    
    # 模拟计算特征
    features = {"average_price": data["price"] * 1.1, "total_volume": data["volume"] * 2}
    print(f"[Process 2] Calculating features: {features}")
    time.sleep(1)  # 模拟计算特征的时间
    queue_out.put(features)  # 将特征字典放入队列

# 进程 3 计算特征的函数
def calculate_features_process3(queue_in):
    features = queue_in.get()  # 等待进程 2 的字典
    print(f"[Process 3] Received features at {datetime.now()}: {features}")
    
    # 模拟进一步处理特征
    final_result = {"final_value": features["average_price"] * 1.5}
    print(f"[Process 3] Final result: {final_result}")

if __name__ == '__main__':
    # 创建进程间通信的队列
    queue1 = Queue()  # 进程 1 到 进程 2
    queue2 = Queue()  # 进程 2 到 进程 3

    # 创建并启动进程
    while True:
        now = datetime.now().time()
        if (now >= datetime.strptime("09:30", "%H:%M").time() and 
            now <= datetime.strptime("11:30", "%H:%M").time()) or \
           (now >= datetime.strptime("13:00", "%H:%M").time() and 
            now <= datetime.strptime("15:00", "%H:%M").time()):
            process1 = Process(target=get_multi_last_price, args=(queue1,))
            process2 = Process(target=calculate_features, args=(queue1, queue2))
            process3 = Process(target=calculate_features_process3, args=(queue2,))

            process1.start()  # 启动进程 1
            process1.join()   # 等待进程 1 完成

            process2.start()  # 启动进程 2
            process2.join()   # 等待进程 2 完成

            process3.start()  # 启动进程 3
            process3.join()   # 等待进程 3 完成
            
        time.sleep(300)  # 每 5 分钟执行一次

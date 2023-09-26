# coding:utf-8
# 策略 双均线

from pickle import TRUE
import backtrader as bt
import pandas as pd
import sys
import backtrader as bt
from backtrader.feeds import PandasData


# class MyCustomIndicator(bt.Indicator):
#     lines = ('my_indicator',)  # 指定自定义指标的输出线

#     def __init__(self):
#         # 初始化指标
#         self.my_indicator = bt.indicators.SimpleMovingAverage(self.data, period=20)  # 使用内置指标作为示例

#     def next(self):
#         # 计算指标的数值
#         self.lines.my_indicator[0] = some_custom_calculation()  # 替换为自定义计算函数

class Addmoredata(PandasData):
    lines = ('K', 'close_rolling_480_std_mean', 'amount_normalize60_rolling_480_mean', 'close6_close96', 'close24_close480', 'close480_close2880', 'close24_close2880')
    params = (('K', 'K'), ('close_rolling_480_std_mean', 'close_rolling_480_std_mean'), 
    ('amount_normalize60_rolling_480_mean', 'amount_normalize60_rolling_480_mean'),
    ('close6_close96', 'close6_close96'),
    ('close24_close480', 'close24_close480'),
    ('close480_close2880', 'close480_close2880'),
    ('close24_close2880', 'close24_close2880'),
    )


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.kdj = bt.indicators.Stochastic(period=9*2, period_dfast=3*2, period_dslow=3*2)

        self.buy_period = "none"
        self.buy_day = None
        self.zhisun = 9999999
        self.skip_num = 0
        self.isbuyaa = False
        self.last_period = None

    # def prenext(self):
    #     if len(self) >= self.skip_num:
    #         self.next()

    def next(self):
        now_day = self.data.datetime.date()
        now_time = self.data.datetime.time()
        # print(datetime)
        # now_day  = datetime.date(0)
        # print(now_time)
        #  self.broker.positions()
        # for position in self.broker.positions:
        #     print(position)
            # print(self.broker.get_position(position).size)

        self.buy_period = "none"
        size = self.broker.get_cash()/self.data.close[0]
        if self.data.K[0] >= 20 and  min(self.data.K.get(size=3)) < 19 and self.data.K[-1] <20:
            self.buy_period = "type1"
            self.last_period = "type1"

        if self.data.K[0] >= 50 and self.data.K[-1] < 50 and self.data.K[-3] < 48:
            if self.last_period == "type2":
                self.buy_period = "type3"
            else:
                self.last_period = "type2"

        if self.data.K[0] <= 80 and self.data.K[-1] > 80:
            if self.data.K[-3]  > 82 or self.data.K[-2]> 82:
                self.buy_period = "typen" 
            self.last_period = "typen"

        if self.buy_period == "type1":
            if self.data.close_rolling_480_std_mean[0] > 0.0 and self.data.close24_close2880  > 0   and (not self.isbuyaa):
                if 1:

                    total_value = self.broker.get_cash()
                    #1手=100股，满仓买入
                    ss=int((total_value/100)/self.datas[0].close[0])*100               

                    print('当前账户余额1:', self.broker.get_cash())
                    print('买入1 {}'.format(ss) )
                    self.order=self.buy(size=ss)
                    # self.buy()
                    print('当前账户余额2:', self.broker.get_cash())
                    # print("buy1 {} {}".format(now_day, now_time))
                    self.buy_day = now_day
                    self.zhisun = min(self.data.low.get(size=5))
                    self.isbuyaa = True

        if self.buy_period == "type3":
            if self.data.close_rolling_480_std_mean[0] > 0.0 and self.data.close24_close2880 > 0  and (not self.isbuyaa) :
                # if self.data.amount_normalize_rolling_480_mean * (self.data.amount_diff_rolling_480_std - 0.72) < -0.015:
                if 1:
                    total_value = self.broker.get_cash()
                    #1手=100股，满仓买入
                    ss=int((total_value/100)/self.datas[0].close[0])*100  

                    self.order = self.buy(size=ss)
                    print('买入3 {}'.format(ss) )
                    # print("buy3 {} {}".format(now_day, now_time))
                    print('当前账户余额:', self.broker.get_cash())
                    self.buy_day = now_day
                    self.zhisun = min(self.data.low.get(size=5))
                    self.isbuyaa = True

        if self.buy_period == "typen":
            if now_day != self.buy_day and self.isbuyaa:
                
                if (self.data.close[0] - self.zhisun)/self.zhisun > 0.03:
                # print('当前账户余额：', self.broker.get_cash())
                #self.sell()
                    self.close(self.datas[0])
                    print("sellzhiyin {} {}".format(now_day, now_time))
                    # print('当前账户：', self.broker.getvalue())
                    self.isbuyaa = False
                    print('当前账户余额：', self.broker.get_cash())
                else:
                    max1 =  max(self.data.close.get(size=5))
                    min1 =  min(self.data.close.get(size=5))
                    #  print("max {} min {}".format(max1, min1))
                    if (max1 - min1)/min1 > 0.002:
                        self.close(self.datas[0])
                        print("sellzhiyin {} {}".format(now_day, now_time))
                        self.isbuyaa = False
                        print('当前账户余额：', self.broker.get_cash())

        else:
            pass


            
        if self.data.close < self.zhisun * 0.995:
            if now_day != self.buy_day and self.isbuyaa:
                print("sellzhisun {} {}".format(now_day, now_time))
                
                self.isbuyaa = False
                # self.sell()
                self.close(self.datas[0])
                # print('当前账户：', self.broker.getvalue())
                print('当前账户余额：', self.broker.get_cash())
        
        # print(self.data.datetime)
        # print(self.position)


if __name__ == '__main__':
    code = sys.argv[1]
    cerebro = bt.Cerebro()
    
    # 读取 csv 数据
    data = pd.read_parquet("/liubinxu/liubinxu/finance/learning/data/{}.qfq.kdj.parquet".format(code))
    # print (data)
    # 将 pandas 数据加载到 backtrader 中
    data["datetime"] = pd.to_datetime(data["datetime"])
    # data = data[480:]
    data_feed = Addmoredata(dataname=data, timeframe = bt.TimeFrame.Minutes)
    
    # 添加数据到 cerebro
    cerebro.adddata(data_feed)

    # 添加策略到 cerebro
    cerebro.addstrategy(MyStrategy)

    # 设置初始资金
    cerebro.broker.setcash(10000.0)

    # 设置交易手续费
    cerebro.broker.setcommission(commission=0)

    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='pnl')  # 返回收益率时序数据
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')  # 年化收益率
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio')  # 夏普比率
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')  # 回撤

    # 运行回测
    result = cerebro.run()

    # 打印回测结果
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    strat = result[0]
    # 返回日度收益率序列
    daily_return = pd.Series(strat.analyzers.pnl.get_analysis())
    # 打印评价指标
    print("--------------- AnnualReturn -----------------")
    print(strat.analyzers._AnnualReturn.get_analysis())
    print("--------------- SharpeRatio -----------------")
    print(strat.analyzers._SharpeRatio.get_analysis())
    print("--------------- DrawDown -----------------")
    print(strat.analyzers._DrawDown.get_analysis())

    cerebro.plot(volume=False, figsize=(100, 10), style='candlestick', show=True)
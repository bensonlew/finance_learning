# coding:utf-8
# 策略 双均线

import backtrader as bt
import pandas as pd

class MyStrategy(bt.Strategy):

    params = (('fast', 240), ('slow', 2400))

    def __init__(self):
        self.fastma = bt.indicators.SMA(self.data.close, period=self.params.fast)
        self.slowma = bt.indicators.SMA(self.data.close, period=self.params.slow)
        self.crossover = bt.indicators.CrossOver(self.fastma, self.slowma)
        self.buy1 = False

    def next(self):
        dt = self.data.datetime.datetime()
        hour = dt.hour
        minute = dt.minute
        # print(minute)
        if hour == 9 and minute == 35:
            # print("start")
            if self.data.volume[0] > self.data.volume[-48] * 1.2 and self.data.low[0] < self.data.close[-1] *0.99 :
                self.buy()
                self.buy1 = True
                print("buy", dt)
                print('当前账户余额：', self.broker.get_cash())

            elif self.data.datetime.date(0) != self.data.datetime.date(-1):
                if self.buy1:
                    print("sell", dt)
                    self.sell()
                    print('当前账户余额：', self.broker.get_cash())
                self.buy1 = False

        # if not self.position:
        #     if self.crossover > 0:
        #         print("buy", dt)

        #         self.buy()
        # elif self.crossover < 0:
        #     print("sell", dt)
        #     self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    
    # 读取 csv 数据
    data = pd.read_parquet("/liubinxu/liubinxu/finance/learning/data/510050.qfq.parquet")
    # print (data)
    # 将 pandas 数据加载到 backtrader 中
    data_feed = bt.feeds.PandasData(dataname=data)
    
    # 添加数据到 cerebro
    cerebro.adddata(data_feed)

    # 添加策略到 cerebro
    cerebro.addstrategy(MyStrategy)

    # 设置初始资金
    cerebro.broker.setcash(1000000.0)

    # 设置交易手续费
    cerebro.broker.setcommission(commission=0.0003)

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

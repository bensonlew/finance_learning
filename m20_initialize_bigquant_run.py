ef m20_initialize_bigquant_run(context):
    # 加载预测数据
    context.ranker_prediction = context.options['data'].read_df()

    # 系统已经设置了默认的交易手续费和滑点，要修改手续费可使用如下函数
    context.set_commission(PerOrder(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    # 预测数据，通过options传入进来，使用 read_df 函数，加载到内存 (DataFrame)
    # 设置买入的股票数量，这里买入预测股票列表排名靠前的5只
    stock_count = 5
    # 每只的股票的权重，如下的权重分配会使得靠前的股票分配多一点的资金，[0.339160, 0.213986, 0.169580, ..]
    context.stock_weights = T.norm([1 / math.log(i + 2) for i in range(0, stock_count)])
    # 设置每只股票占用的最大资金比例
    context.max_cash_per_instrument = 0.2
    context.hold_days = 5

# 回测引擎：每日数据处理函数，每天执行一次
def m20_handle_data_bigquant_run(context, data):
    # 按日期过滤得到今日的预测数据
    ranker_prediction = context.ranker_prediction[
        context.ranker_prediction.date == data.current_dt.strftime('%Y-%m-%d')]

    # 1. 资金分配
    # 平均持仓时间是hold_days，每日都将买入股票，每日预期使用 1/hold_days 的资金
    # 实际操作中，会存在一定的买入误差，所以在前hold_days天，等量使用资金；之后，尽量使用剩余资金（这里设置最多用等量的1.5倍）
    is_staging = context.trading_day_index < context.hold_days # 是否在建仓期间（前 hold_days 天）
    cash_avg = context.portfolio.portfolio_value / context.hold_days
    cash_for_buy = min(context.portfolio.cash, (1 if is_staging else 1.5) * cash_avg)
    cash_for_sell = cash_avg - (context.portfolio.cash - cash_for_buy)
    positions = {e.symbol: p.amount * p.last_sale_price
                 for e, p in context.perf_tracker.position_tracker.positions.items()}

    # 2. 生成卖出订单：hold_days天之后才开始卖出；对持仓的股票，按StockRanker预测的排序末位淘汰
    if not is_staging and cash_for_sell > 0:
        equities = {e.symbol: e for e, p in context.perf_tracker.position_tracker.positions.items()}
        instruments = list(reversed(list(ranker_prediction.instrument[ranker_prediction.instrument.apply(
                lambda x: x in equities and not context.has_unfinished_sell_order(equities[x]))])))
        for instrument in instruments:
            context.order_target(context.symbol(instrument), 0)
            cash_for_sell -= positions[instrument]
            if cash_for_sell <= 0:
                break
    #---------------------START：大盘风控(含建仓期)--------------------------
    today_date = data.current_dt.strftime('%Y-%m-%d')
    positions_all = [equity.symbol for equity in context.portfolio.positions]
    dataprediction=context.dataprediction
    today_prediction=dataprediction[dataprediction.date==today_date].direction.values[0]
    # 满足空仓条件
    if today_prediction<0:	
        if len(positions_all)>0:
            # 全部卖出后返回
            for i in positions_all:
                if data.can_trade(context.symbol(i)):
                    context.order_target_percent(context.symbol(i), 0)
                    print('风控执行',today_date)
                    return
                #运行风控后当日结束，不再执行后续的买卖订单
    #------------------------END：大盘风控(含建仓期)---------------------------
    
    # 3. 生成买入订单：按StockRanker预测的排序，买入前面的stock_count只股票
    buy_cash_weights = context.stock_weights
    buy_instruments = list(ranker_prediction.instrument[:len(buy_cash_weights)])
    max_cash_per_instrument = context.portfolio.portfolio_value * context.max_cash_per_instrument
    for i, instrument in enumerate(buy_instruments):
        cash = cash_for_buy * buy_cash_weights[i]
        if cash > max_cash_per_instrument - positions.get(instrument, 0):
            # 确保股票持仓量不会超过每次股票最大的占用资金量
            cash = max_cash_per_instrument - positions.get(instrument, 0)
        if cash > 0:
            context.order_value(context.symbol(instrument), cash)

# 回测引擎：准备数据，只执行一次
def m20_prepare_bigquant_run(context):
    seq_len=5    #每个input的长度
    # 导入包
    from keras.layers.core import Dense, Activation, Dropout
    from keras.layers.recurrent import LSTM
    from keras.models import Sequential
    from keras import optimizers
    import tensorflow.keras as tf   
    from sklearn.preprocessing import scale
    from tensorflow.keras.layers import Input, Dense, LSTM
    from tensorflow.keras.models import Model
    # 基础参数配置
    instrument = '000300.SHA'  #股票代码
    #设置用于训练和回测的开始/结束日期
    train_length=seq_len*10
    start_date_temp= (pd.to_datetime(context.start_date) - datetime.timedelta(days=2*train_length)).strftime('%Y-%m-%d') # 多取几天的数据,这里取5倍
    len1=len(D.trading_days(start_date=start_date_temp, end_date=context.end_date)) 
    len2=len(D.trading_days(start_date=context.start_date, end_date=context.end_date))
    distance=len1-len2
    trade_day=D.trading_days(start_date=start_date_temp, end_date=context.end_date)
    start_date = trade_day.iloc[distance-train_length][0].strftime('%Y-%m-%d')
    split_date = trade_day.iloc[distance-1][0].strftime('%Y-%m-%d')
    fields = ['close', 'open', 'high', 'low', 'amount', 'volume']  # features因子
    batch = 100#整数，指定进行梯度下降时每个batch包含的样本数,训练时一个batch的样本会被计算一次梯度下降，使目标函数优化一步
    
    # 数据导入以及初步处理
    data1 = D.history_data(instrument, start_date, context.end_date, fields)
    data1['return'] = data1['close'].shift(-5) / data1['open'].shift(-1) - 1 #计算未来5日收益率（未来第五日的收盘价/明日的开盘价）
    data1=data1[data1.amount>0]
    datatime = data1['date'][data1.date>split_date]  #记录predictions的时间，回测要用
    data1['return'] = data1['return']
    data1['return'] = data1['return']*10  # 适当增大return范围，利于LSTM模型训练
    data1.reset_index(drop=True, inplace=True)
    scaledata = data1[fields]
    traindata = data1[data1.date<=split_date]
    
    # 数据处理：设定每个input（series×6features）以及数据标准化
    train_input = []
    train_output = []
    test_input = []
    for i in range(seq_len-1, len(traindata)):
        a = scale(scaledata[i+1-seq_len:i+1])
        train_input.append(a)
        c = data1['return'][i]
        train_output.append(c)
    for j in range(len(traindata), len(data1)):
        b = scale(scaledata[j+1-seq_len:j+1])
        test_input.append(b)


    # LSTM接受数组类型的输入
    train_x = np.array(train_input)
    train_y = np.array(train_output)
    test_x = np.array(test_input) 

    # 自定义激活函数
    import tensorflow.keras as tf
    def atan(x): 
        return tf.atan(x)
    # 构建神经网络层 1层LSTM层+3层Dense层
    # 用于1个输入情况
    lstm_input = Input(shape=(seq_len,len(fields)), name='lstm_input')
    lstm_output = LSTM(32,input_shape=(seq_len,len(fields)))(lstm_input)
    Dense_output_1 = Dense(16, activation='linear')(lstm_output)
    Dense_output_2 = Dense(4, activation='linear')(Dense_output_1)
    predictions = Dense(1)(Dense_output_2)
    model = Model(inputs=lstm_input, outputs=predictions)
    model.compile(optimizer='adam', loss='mse', metrics=['mse'])
    model.fit(train_x, train_y, batch_size=batch, nb_epoch=5, verbose=0)
    # 预测
    predictions = model.predict(test_x)
    # 如果预测值>0,取为1；如果预测值<=0,取为-1.为回测做准备
    for i in range(len(predictions)):
        if predictions[i]>0:
            predictions[i]=1
        elif predictions[i]<=0:
            predictions[i]=-1
            
    # 将预测值与时间整合作为回测数据
    cc = np.reshape(predictions,len(predictions), 1)
    dataprediction = pd.DataFrame()
    dataprediction['date'] = datatime
    dataprediction['direction']=np.round(cc)
    context.dataprediction=dataprediction


m1 = M.instruments.v2(
    start_date='2017-06-01',
    end_date='2017-07-01',
    market='CN_STOCK_A',
    instrument_list='',
    max_count=0
)

m2 = M.advanced_auto_labeler.v2(
    instruments=m1.data,
    label_expr="""# #号开始的表示注释
# 0. 每行一个，顺序执行，从第二个开始，可以使用label字段
# 1. 可用数据字段见 https://bigquant.com/docs/data_history_data.html
#   添加benchmark_前缀，可使用对应的benchmark数据
# 2. 可用操作符和函数见 `表达式引擎 <https://bigquant.com/docs/big_expr.html>`_

# 计算收益：5日收盘价(作为卖出价格)除以明日开盘价(作为买入价格)
shift(close, -5) / shift(open, -1)

# 极值处理：用1%和99%分位的值做clip
clip(label, all_quantile(label, 0.01), all_quantile(label, 0.99))

# 将分数映射到分类，这里使用20个分类
all_wbins(label, 20)

# 过滤掉一字涨停的情况 (设置label为NaN，在后续处理和训练中会忽略NaN的label)
where(shift(high, -1) == shift(low, -1), NaN, label)
""",
    start_date='',
    end_date='',
    benchmark='000300.SHA',
    drop_na_label=True,
    cast_label_int=True
)

m3 = M.input_features.v1(
    features="""# #号开始的表示注释
# 多个特征，每行一个，可以包含基础特征和衍生特征
rank_avg_amount_5
rank_avg_turn_5
rank_volatility_5_0
rank_swing_volatility_5_0
rank_avg_mf_net_amount_5"""
)

m15 = M.general_feature_extractor.v7(
    instruments=m1.data,
    features=m3.data,
    start_date='',
    end_date='',
    before_start_days=300
)

m16 = M.derived_feature_extractor.v3(
    input_data=m15.data,
    features=m3.data,
    date_col='date',
    instrument_col='instrument',
    drop_na=False,
    remove_extra_columns=False,
    user_functions={}
)

m7 = M.join.v3(
    data1=m2.data,
    data2=m16.data,
    on='date,instrument',
    how='inner',
    sort=False
)

m12 = M.dropnan.v1(
    input_data=m7.data
)

m17 = M.stock_ranker_train.v6(
    training_ds=m12.data,
    features=m3.data,
    learning_algorithm='排序',
    number_of_leaves=30,
    minimum_docs_per_leaf=1000,
    number_of_trees=20,
    learning_rate=0.1,
    max_bins=1023,
    feature_fraction=1,
    data_row_fraction=1,
    ndcg_discount_base=1,
    m_lazy_run=False
)

m9 = M.instruments.v2(
    start_date=T.live_run_param('trading_date', '2017-07-01'),
    end_date=T.live_run_param('trading_date', '2018-04-30'),
    market='CN_STOCK_A',
    instrument_list='',
    max_count=0
)

m18 = M.general_feature_extractor.v7(
    instruments=m9.data,
    features=m3.data,
    start_date='',
    end_date='',
    before_start_days=300
)

m19 = M.derived_feature_extractor.v3(
    input_data=m18.data,
    features=m3.data,
    date_col='date',
    instrument_col='instrument',
    drop_na=False,
    remove_extra_columns=False
)

m13 = M.dropnan.v1(
    input_data=m19.data
)

m8 = M.stock_ranker_predict.v5(
    model=m17.model,
    data=m13.data,
    m_lazy_run=False
)

m20 = M.trade.v4(
    instruments=m9.data,
    options_data=m8.predictions,
    start_date='',
    end_date='',
    initialize=m20_initialize_bigquant_run,
    handle_data=m20_handle_data_bigquant_run,
    prepare=m20_prepare_bigquant_run,
    volume_limit=0.025,
    order_price_field_buy='open',
    order_price_field_sell='close',
    capital_base=1000001,
    auto_cancel_non_tradable_orders=True,
    data_frequency='daily',
    price_type='后复权',
    product_type='股票',
    plot_charts=True,
    backtest_only=False,
    benchmark='000300.SHA'
)
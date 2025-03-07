# 重新加载必要的库
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import mplfinance as mpf
import numpy as np
# 重新读取用户上传的 K 线数据文件
file_path_kline = "D:/code/vis/data/EURUSDx_M15_202204010000_202409240645.csv"
df_kline = pd.read_csv(file_path_kline, sep="\t")

# df_kline.columns
# 解析时间字段
df_kline['datetime'] = pd.to_datetime(
    df_kline['<DATE>'] + ' ' + df_kline['<TIME>'])
df_kline.set_index('datetime', inplace=True)

# 选择需要的列，并转换为浮点数
ohlc_df = df_kline[['<OPEN>', '<HIGH>',
                    '<LOW>', '<CLOSE>']].astype(float).copy()

# 仅绘制最近 500 根 K 线
ohlc_df = ohlc_df.iloc[-500:]

# 设置绘图
fig, ax = plt.subplots(figsize=(12, 6))

# 颜色设置
color_up = 'green'   # 收盘价高于开盘价（上涨K线）
color_down = 'red'   # 收盘价低于开盘价（下跌K线）

# 绘制K线
for idx, row in ohlc_df.iterrows():
    date = row.name  # datetime 索引
    open_price = row['<OPEN>']
    high_price = row['<HIGH>']
    low_price = row['<LOW>']
    close_price = row['<CLOSE>']

    # 颜色判断
    color = color_up if close_price >= open_price else color_down

    # 画K线的影线（高低价格）
    ax.plot([date, date], [low_price, high_price], color='black', linewidth=1)

    # 画K线的实体（开盘价-收盘价）
    rect = Rectangle((mdates.date2num(date) - 0.003, min(open_price, close_price)),
                     0.006, abs(close_price - open_price),
                     facecolor=color, edgecolor='black')
    ax.add_patch(rect)

# 设置时间格式
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
plt.xticks(rotation=45)

# 添加标题和标签
ax.set_title("EUR/USD 15-Minute K-Line Chart (Last 500 Candles)")
ax.set_xlabel("Time")
ax.set_ylabel("Price")

# 显示图表
plt.grid()
plt.show()

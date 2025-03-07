import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import numpy as np

# 1. 讀取 K 線數據文件
file_path_kline = "./data/EURUSDx_M15_202204010000_202409240645.csv"
df_kline = pd.read_csv(file_path_kline, sep="\t")

# 檢查文件是否成功讀取
if df_kline.empty:
    raise ValueError("CSV 文件為空，請檢查檔案內容是否正確")

# 列印資料內容
#print(df_kline.head())
#print(df_kline.columns)

# 2. 新增 'f_signals' 欄位
np.random.seed(42)  # 固定隨機種子以便結果可重現
df_kline['f_signals'] = np.random.randint(-2, 4, size=len(df_kline))

# 列印新增後的資料框確認
#print(df_kline.head())

# 3. 解析時間字段
df_kline['datetime'] = pd.to_datetime(df_kline['<DATE>'] + ' ' + df_kline['<TIME>'])
df_kline.set_index('datetime', inplace=True)

# 4. 確保列名存在於資料框中
required_columns = ['<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', 'f_signals']
for col in required_columns:
    if col not in df_kline.columns:
        raise KeyError(f"資料框中缺少必要的列：{col}")

# 列印確認所有必要欄位
#print("資料框的所有欄位：", df_kline.columns)

# 5. 選擇需要的列
ohlc_df = df_kline[['<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', 'f_signals']].astype(float)

# 僅繪製最近 500 根 K 線
ohlc_df = ohlc_df.iloc[-500:]

# 6. 繪製 K 線圖
fig, ax = plt.subplots(figsize=(12, 6))

# 設置顏色
color_up = 'green'
color_down = 'red'

# 固定標記符號的偏移距離
offset = 0.0005

# 繪製 K 線
for idx, row in ohlc_df.iterrows():
    date = row.name
    open_price = row['<OPEN>']
    high_price = row['<HIGH>']
    low_price = row['<LOW>']
    close_price = row['<CLOSE>']
    signal = row['f_signals']
    
    # 設置顏色
    color = color_up if close_price >= open_price else color_down
   
    # 繪製影線
    ax.plot([date, date], [low_price, high_price], color='black', linewidth=1)
    
    # 繪製實體
    rect = Rectangle((mdates.date2num(date) - 0.003, min(open_price, close_price)),
                     0.006, abs(open_price - close_price),
                     facecolor=color, edgecolor='black')
    ax.add_patch(rect)
    
    # 根據 f_signals 加入標記
    if signal > 0:
        ax.text(mdates.date2num(date), low_price - offset,
                "^", color='blue', fontsize=10, ha='center', va='center', fontweight='bold')
    elif signal < 0:
        ax.text(mdates.date2num(date), high_price + offset,
                "v", color='red', fontsize=10, ha='center', va='center', fontweight='bold')

# 設置時間格式
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
plt.xticks(rotation=45)

# 添加標題和標籤
ax.set_title("EUR/USD 15-Minute K-Line Chart (Last 500 Candles)")
ax.set_xlabel("Time")
ax.set_ylabel("Price")

# 顯示圖表
plt.grid()
plt.show()

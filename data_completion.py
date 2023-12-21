import pandas as pd
import numpy as np

# 读取excel文件
df = pd.read_excel('宋浩高数观看数据.xlsx', sheet_name='按照同一时间累加')

# 遍历每一列
for col in df.columns:
    # 遍历每一行
    for i in range(len(df)):
        # 如果当前单元格值为"-"
        if df.loc[i, col] == "-":
            # 查找上下单元格的值
            above = df.loc[i-1, col] if i > 0 else np.nan
            below = df.loc[i+1, col] if i < len(df)-1 else np.nan

            # 如果上下单元格都是数字，则取平均值并四舍五入
            if pd.to_numeric(above, errors='coerce') is not np.nan and pd.to_numeric(below, errors='coerce') is not np.nan:
                df.loc[i, col] = round((float(above) + float(below)) / 2)

# 将处理后的数据保存到新的excel文件
df.to_excel('new_file.xlsx', index=False)

import pandas as pd
import numpy as np

# 读取excel文件
df = pd.read_excel('宋浩高数观看数据.xlsx', sheet_name='按照同一时间累加')

# 将时间列转换为datetime类型，并设置为索引
df['时间'] = pd.to_datetime(df['时间'])
df.set_index('时间', inplace=True)

# 使用resample函数按30分钟的时间段进行重采样，并计算每个时间段的平均值
df_resampled = df.resample('30T').mean()

# 对结果保留1位有效数字
df_resampled = df_resampled.round(1)

# 创建一个ExcelWriter对象，并设置为在新文件上写入
writer = pd.ExcelWriter('宋浩高数观看数据_合并后.xlsx', engine='openpyxl') 

# 将处理后的数据写入到新文件的'按照同一时间累加合并后'工作表
df_resampled.reset_index().to_excel(writer, index=False, sheet_name='按照同一时间累加合并后')

# 保存新文件
# writer.save()
writer.close()

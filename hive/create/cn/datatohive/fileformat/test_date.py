import locale
from datetime import datetime
import pandas as pd

# 使用字符串指定起始日期和结束日期
date_range = pd.date_range(start='2023-01-01', end='2023-01-10')
print(date_range)

# 指定生成 5 个日期
date_range = pd.date_range(start='2023-01-01', periods=5)
print(date_range)

# 指定每周的星期一\W-SUN：每周的星期日。\W-SAT：每周的星期六。
# Q 频率字符串后面可以跟上一个正整数，表示第几个季度。例如，Q1 表示第一个季度，Q2 表示第二个季度，以此类推。
# 要指定每个月的第几周，你可以使用 freq 参数中的 W 频率字符串，后跟一个正整数，表示每个月的第几周。例如，W-1 表示每个月的第一个周，W-2 表示每个月的第二个周，以此类推。
date_range = pd.date_range(start='2023-01-01', end='2023-01-31', freq='W-1')
print(date_range)

# 指定时区为 UTC
date_range = pd.date_range(start='2023-01-01', end='2023-01-10', tz='UTC')
print(date_range)

# 设置 normalize 为 True
date_range = pd.date_range(start='2023-01-01 08:00:00', end='2023-01-05 12:00:00', normalize=True)
print(date_range)

# 设置时间索引的名称为 'dates'
date_range = pd.date_range(start='2023-01-01', end='2023-01-05', name='dates')
print(date_range)

# 包含开始日期但不包含结束日期
date_range = pd.date_range(start='2023-01-01', end='2023-01-05', closed='left')
print(date_range)

# 生成日期数据
start_date = datetime(2021, 1, 1)
end_date = datetime(2021, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date)
print(date_range)
locale.setlocale(locale.LC_CTYPE, 'Chinese')
    # 插入数据
    # 2021 2021-10 4 42周 星期日 2021-10-10 yes no 周末
for date in date_range:
    date_id = date.strftime('%Y%m%d')
    year_name_cn = date.strftime('%Y年')
    print(date.dayofweek)
    print(date_id)
    print(year_name_cn)
for dt in date_range:
    date = dt.date()
    if date in (datetime.strptime(d, '%Y-%m-%d').date() for d in('2021-01-01', '2021-02-11', '2021-02-12', '2021-02-13',
                '2021-02-14', '2021-02-15', '2021-02-16', '2021-02-17', '2021-04-04',
                '2021-04-05', '2021-04-06', '2021-05-01', '2021-05-02', '2021-05-03',
                '2021-06-14', '2021-06-15', '2021-06-16', '2021-09-21', '2021-09-22',
                '2021-09-23', '2021-10-01', '2021-10-02', '2021-10-03', '2021-10-04',
                '2021-10-05', '2021-10-06', '2021-10-07')):
            is_workday = 'n'
    elif dt.dayofweek + 1 in (0, 5):
         is_workday = 'y'
    else:
            is_workday = 'None'
    print(is_workday)
print(date_range)
print(pd.Series(date_range))
# 获取每周的范围
weekly_ranges = [(w,w+pd.offsets.Week(weekday=6))for w in pd.Series(date_range)]
print(weekly_ranges)
ranges =weekly_ranges.apply(lambda x: x - pd.offsets.Week(weekday=6))

# 打印每周的范围
for start, end in weekly_ranges:
    print("Week start:", start, "Week end:", end)
# 创建日期范围
date_range = pd.date_range(start=start_date, end=end_date, freq='Q')
print(date_range)
# 获取每个季度的起始日期和结束日期
for quarter_start in date_range:
    quarter_end = quarter_start + pd.offsets.QuarterEnd()
    print("季度起始日期:", quarter_start.date())
    print("季度结束日期:", quarter_end.date())

# 获取日期范围中每个季度的起始和结束日期
def get_quarter_dates(start_date, end_date):
    quarters = pd.date_range(start=start_date, end=end_date, freq='Q')
    quarter_dates = [(q,q+pd.offsets.QuarterEnd()) for q in quarters]
    print(quarter_dates)
    return quarter_dates

# 判断日期所在的季度
def get_quarter(date,start_date,end_date):
    quarter_dates = get_quarter_dates(start_date, end_date)  # 假设是2023年的日期范围
    print(quarter_dates)
    for i, (start, end) in enumerate(quarter_dates, start=2):
        print((start, end))
        if date<start :
            return i-1
        elif start <= date <= end:
            return i
    return None  # 如果日期不在任何季度范围内，则返回None

# 测试示例
date = pd.to_datetime('2021-01-04')
quarter = get_quarter(date,'2021-01-01','2021-12-31')
if quarter:
    print(f"{date} 是第 {quarter} 季度")
else:
    print("日期不在任何季度范围内")
# 获取每个月的第一天
monthly_dates = date_range.to_period('M').start_time.drop_duplicates()
print("\n每个月的第一个日期：")
print(monthly_dates)
date = '2021-02-11'
if date in ('2021-01-01', '2021-02-11', '2021-02-12', '2021-02-13',
            '2021-02-14', '2021-02-15', '2021-02-16', '2021-02-17', '2021-04-04',
            '2021-04-05', '2021-04-06', '2021-05-01', '2021-05-02', '2021-05-03',
            '2021-06-14', '2021-06-15', '2021-06-16', '2021-09-21', '2021-09-22',
            '2021-09-23', '2021-10-01', '2021-10-02', '2021-10-03', '2021-10-04',
            '2021-10-05', '2021-10-06', '2021-10-07'):
    is_workday = 'y'
elif date.dayofweek + 1 in (0, 5):
    is_workday = 'y'
else:
    is_workday = 'n'
print(is_workday)
# 指定日期列表
date_list = ['2023-01-03', '2023-01-05', '2023-01-07']
# 检查日期范围中的日期是否包含在指定的日期列表中
result = date_range.isin(date_list)
print('结果：', result)

# 获取每个周末的日期
print(date_range.dayofweek)
weekend_dates = date_range[date_range.dayofweek.isin([5, 6])]
print("\n每个周末的日期：")
print(date_range.dayofweek.isin([5, 6])[0])
print(weekend_dates)
# 获取每个周末的日期
weekend_dates = date_range[date_range.dayofweek.isin([0, 4])]
print("\n每个工作日的日期：")
print(weekend_dates)
#!/usr/bin/env python
# @desc : todo ODS&DWD建库、建表、装载数据主类
__coding__ = "utf-8"
__author__ = "fmg"

from datetime import datetime
import pandas as pd
import locale

# 根据不同功能接口记录不同的日志
from hive.create.cn.config import common
from hive.create.cn.datatohive.utils import OracleHiveUtil

admin_logger = common.get_logger('fmg14')


def recordLog(modelName):
    """
    记录普通级别日志
    :param modelName: 模块名称
    :return: 日志信息
    """
    msg = f'{modelName}'
    admin_logger.info(msg)
    return msg


def recordWarnLog(msg):
    """
    记录警告级别日志
    :param msg: 日志信息
    :return: 日志信息
    """
    admin_logger.warning(msg)
    return msg

# # 获取日期范围中每个季度的起始和结束日期
def get_quarter_dates(start_date, end_date):
    quarters = pd.date_range(start=start_date, end=end_date, freq='Q')
    quarter_dates = [(q,q+pd.offsets.QuarterEnd()) for q in quarters]
    print(quarter_dates)
    return quarter_dates

# 判断日期所在的季度
def get_quarter(date,start_date,end_date):
    quarter_dates = get_quarter_dates(start_date, end_date)  # 假设是2023年的日期范围
    for i, (start, end) in enumerate(quarter_dates, start=2):
        print((start, end))
        if date < start:
            return i - 1
        elif start <= date <= end:
            return i
    return None  # 如果日期不在任何季度范围内，则返回None


# # 获取日期范围中每个周的起始和结束日期
def get_week_dates(start_date, end_date):
    weeks = pd.date_range(start=start_date, end=end_date, freq='W')
    quarter_dates = [(w,w+pd.offsets.Week(weekday=6))for w in pd.Series(weeks)]
    print(quarter_dates)
    return quarter_dates
# 判断日期所在的周
def get_week(date,start_date,end_date):
    Week_dates = get_week_dates(start_date, end_date)
    for i, (start, end) in enumerate(Week_dates, start=2):
        if date < start:
            return i - 1
        elif start <= date <= end:
            return i
    return None  # 如果日期不在任何周范围内，则返回None

# # 将星期几转换为英文
# def translate_week(weekday):


if __name__ == '__main__':

    # =================================todo: 1-初始化Oracle、Hive连接，读取表的名称=========================#

    recordLog('Building 时间维度表')
    partitionVal = '20210101'
    # oracleConn = OracleHiveUtil.getOracleConn()
    hiveConn = OracleHiveUtil.getSparkHiveConn()
    # tableName = 'dim_date'
    # 创建游标
    cursor = hiveConn.cursor()
    # 创建时间维度表的建表语句
    drop_table_query=""" drop table if exists one_make_dws.dim_date"""
    create_table_query = """
    CREATE EXTERNAL TABLE IF NOT EXISTS one_make_dws.dim_date(
    date_id string comment '日期id',
    year_name_cn string comment '年份名称（中文）',
    year_month_id string comment '年月id',
    year_month_cn string comment '年月（中文）',
    quota_id string comment '季度id',
    quota_namecn string comment '季度名称（中文）',
    quota_nameen string comment '季度名称（英文）',
    quota_shortnameen string comment '季度名称（英文简写）',
    week_in_year_id string comment '周id',
    week_in_year_name_cn string comment '周（中文）',
    week_in_year_name_en string comment '周（英文）',
    weekday int comment '星期',
    weekday_cn string comment '星期（中文）',
    weekday_en string comment '星期（英文）',
    weekday_short_name_en string comment '星期（英文缩写）',
    yyyymmdd string comment '日期_yyyy_mm_dd',
    yyyymmdd_cn string comment '日期中文',
    is_workday string comment '是否工作日',
    is_weekend string comment '是否周末',
    is_holiday string comment '是否法定节假日',
    date_type string comment '日期类型'
    ) COMMENT '时间维度表'
    partitioned by (year integer)
    STORED AS ORC
    LOCATION '/data/dw/dws/one_make/dim_date'
    TBLPROPERTIES ("orc.compress"="SNAPPY")
    """
    alter_partiton = """
            alter table one_make_dws.dim_date add if not exists partition
        (year='2021') location '/data/dw/dws/one_make/dim_date/year=2021'
    """
    # 执行建表语句
    cursor.execute(drop_table_query)
    cursor.execute(create_table_query)
    cursor.execute(alter_partiton)
    hiveConn.commit()
    # 生成日期数据
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2021, 12, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='d')
    locale.setlocale(locale.LC_CTYPE, 'Chinese')
    # 插入数据
    # 2021 2021-10 4 42周 星期日 2021-10-10 yes no 周末
    for date in date_range:
        date_id = date.strftime('%Y%m%d')
        year_name_cn = date.strftime('%Y年')
        year_month_id = date.strftime('%Y%m')
        year_month_cn = date.strftime('%Y年%m月')
        #季度id
        # 获取每个季度的第一天
        quarter = get_quarter(date, '2021-01-01', '2021-12-31')
        quota_id =date.strftime("%YQ") + str(quarter)

        # 季度名称（中文）',
        quota_namecn=f"第 {quarter} 季度"
        # '季度名称（英文）'
        quota_nameen= date.strftime("%Y Q") + str(quarter)
        # '季度名称（英文简写）',
        quota_shortnameen=f"Q{quarter}"
        # '周id',
        week=get_week(date, '2021-01-01', '2021-12-31')
        week_in_year_id =date.strftime("%YW") + str(week)
        # '周（中文）',
        week_in_year_name_cn=date.strftime("%Y")+f"第{week}周"
        # '周（英文）',
        week_in_year_name_en =date.strftime("%Y")+f" W{week}"
        # '星期',   int
        weekday = int(date.weekday()+1)
        # 将数字转换为星期几的文本表示形式
        weekdays_en = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekdays_short=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        weekdays_cn = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
        # '星期（中文）'
        weekday_cn = weekdays_cn[weekday-1]
        # '星期（英文）',
        weekday_en= weekdays_en[weekday-1]
        # '星期（英文缩写）',
        weekday_short_name_en= weekdays_short[weekday-1]
        # '日期_yyyy_mm_dd',
        yyyymmdd= date.strftime('%Y_%m_%d')
        # '日期中文',
        yyyymmdd_cn= date.strftime('%Y年%m月%d日')
        # '是否工作日',

        dt = date.date()
        if dt in (datetime.strptime(d, '%Y-%m-%d').date() for d in
                    ('2021-01-01', '2021-02-11', '2021-02-12', '2021-02-13',
                     '2021-02-14', '2021-02-15', '2021-02-16', '2021-02-17', '2021-04-04',
                     '2021-04-05', '2021-04-06', '2021-05-01', '2021-05-02', '2021-05-03',
                     '2021-06-14', '2021-06-15', '2021-06-16', '2021-09-21', '2021-09-22',
                     '2021-09-23', '2021-10-01', '2021-10-02', '2021-10-03', '2021-10-04',
                     '2021-10-05', '2021-10-06', '2021-10-07')):
            is_workday = 'n'
        elif date.dayofweek  in range(0, 5):
            is_workday = 'y'
        else:
            is_workday = 'n'
        # '是否周末',
        if date.dayofweek in range(5, 7) :
            is_weekend= 'y'
        else:
            is_weekend = 'n'
        # '是否法定节假日',
        # 法定节假日日期：
        # ['2021-01-01','2021-02-11', '2021-02-12', '2021-02-13', '2021-02-14', '2021-02-15', '2021-02-16', '2021-02-17','2021-04-04', '2021-04-05', '2021-04-06','2021-05-01', '2021-05-02', '2021-05-03','2021-06-14', '2021-06-15', '2021-06-16','2021-09-21', '2021-09-22', '2021-09-23','2021-10-01', '2021-10-02', '2021-10-03', '2021-10-04', '2021-10-05', '2021-10-06', '2021-10-07']
        if dt in (datetime.strptime(d, '%Y-%m-%d').date() for d in
                  ('2021-01-01', '2021-02-11', '2021-02-12', '2021-02-13',
                   '2021-02-14', '2021-02-15', '2021-02-16', '2021-02-17', '2021-04-04',
                   '2021-04-05', '2021-04-06', '2021-05-01', '2021-05-02', '2021-05-03',
                   '2021-06-14', '2021-06-15', '2021-06-16', '2021-09-21', '2021-09-22',
                   '2021-09-23', '2021-10-01', '2021-10-02', '2021-10-03', '2021-10-04',
                   '2021-10-05', '2021-10-06', '2021-10-07')):
                    is_holiday= 'y'
        else :
                    is_holiday = 'n'

        # '日期类型'
        if is_holiday== 'y' :
                date_type= '法定节假日'
        elif is_weekend== 'y':
                date_type = '周末'
        else:
                date_type = '工作日'
        insert_query = f"""
        INSERT into TABLE one_make_dws.dim_date 
        PARTITION (year='2021')
        VALUES ('{date_id}', '{year_name_cn}', '{year_month_id}', '{year_month_cn}','{quota_id}', '{quota_namecn}','{quota_nameen}',
        '{quota_shortnameen}','{week_in_year_id}','{week_in_year_name_cn}','{week_in_year_name_en}',{weekday},'{weekday_cn}','{weekday_en}',
        '{weekday_short_name_en}','{yyyymmdd}','{yyyymmdd_cn}','{is_workday}','{is_weekend}','{is_holiday}','{date_type}')
        """
        cursor.execute(insert_query)
    hiveConn.close()




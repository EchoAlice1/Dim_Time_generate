hive数仓时间维度表的创建
表格格式如下：
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
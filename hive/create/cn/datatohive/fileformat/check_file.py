from pyarrow import fs, orc

# 创建 Hadoop 文件系统（HDFS）
hdfs = fs.HadoopFileSystem(host='hadoop.bigdata.cn', port=9000, user='root')

# 指定 ORC 文件路径
orc_file_path = '/data/dw/dws/one_make/dim_date/2021/part-00000-cf2fc4b3-7485-4861-81e7-da0c3f76e6de-c000.snappy.orc'

# 从 HDFS 中读取 ORC 文件
with hdfs.open(orc_file_path, 'rb') as f:
    # 读取 ORC 文件
    orc_table = orc.ORCFile(f).read()

# 将 ORC 文件内容转换为 Pandas DataFrame
df = orc_table.to_pandas()

# 打印 DataFrame
print(df)

############# 数据库相关配置 #####################
mysql_host = '127.0.0.1'
mysql_port = 3306
mysql_user = 'root'
mysql_pwd = 'Delete1350'
mysql_db = 'ideaman'


############# 爬虫下载文件相关配置 #####################
download_files_paths = [
    '/home/ideaman-data/pdf/',  # pdf 存储路径
    '/home/ideaman-data/text/',  # 文本目录
    '/home/ideaman-data/thumbs/'  # 缩略图路径
]

############# 下载历史数据 #####################
start_date_str = "1999-01-01"
end_date_str = "2021-04-01"

############# Milvus #####################
milvus_ip = '1.14.43.148'

############## ES #####################
es_ip = mysql_host

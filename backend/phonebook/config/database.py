from pymongo import MongoClient

# 创建MongoDB客户端连接
client = MongoClient("mongodb+srv://admin:admin@hins.fdmah.mongodb.net/?retryWrites=true&w=majority&appName=hins")

# 选择数据库
db = client.contacts

# 选择集合(相当于关系型数据库中的表)
collection_name = db["contacts list"]
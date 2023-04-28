import pandas as pd
import sqlite3

# 连接到 SQLite 数据库
conn = sqlite3.connect('example.db')

# 创建一个表格
create_table_query = 'CREATE TABLE IF NOT EXISTS mytable (id integer primary key, name text, age integer)'
conn.execute(create_table_query)

# 插入数据
data = {'name': ['Alice', 'Bob', 'Charlie'], 'age': [25, 30, 35]}
df = pd.DataFrame(data)
df.to_sql('mytable', conn, if_exists='append', index=False)

# 查询数据
query = 'SELECT * FROM mytable'
results = pd.read_sql(query, conn)
print(results)

# 更新数据
update_query = "UPDATE mytable SET age=40 WHERE name='Bob'"
conn.execute(update_query)

# 再次查询数据，验证更新操作是否成功
results = pd.read_sql(query, conn)
print(results)

# 删除数据
delete_query = "DELETE FROM mytable WHERE name='Charlie'"
conn.execute(delete_query)

# 再次查询数据，验证删除操作是否成功
results = pd.read_sql(query, conn)
print(results)

# 关闭数据库连接
conn.close()

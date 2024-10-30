from neo4j import GraphDatabase

'''
将数据导入到Neo4j中
'''



# Neo4j连接参数
uri = "bolt://localhost:7687"
username = "neo4j"
password = "lzh10172418"

# 打开你的TXT文件
with open('testdata.txt', 'r') as file:
    lines = file.readlines()

# 创建一个Neo4j驱动对象
driver = GraphDatabase.driver(uri, auth=(username, password))

# 创建一个会话来执行Cypher查询
with driver.session() as session:
    for line in lines:
        # 解析每一行的有效信息
        parts = line.strip().split()
        if len(parts) >= 4:
            person1_id = parts[0]
            person2_id = parts[1]
            relation_type = parts[-1].lower()  # 转换为小写以统一处理

            # 根据relation_type创建不同类型的边
            if relation_type == 'm':
                relationship = ":MOTHER_OF"
            elif relation_type == 'f':
                relationship = ":FATHER_OF"
            elif relation_type == 's':
                relationship = ":SPOUSE_OF"
            else:
                print(f"Unknown relation type: {relation_type}")
                continue

            # 创建或获取节点，并创建带有标签的关系
            query = f"""
            MERGE (p1:Person {{ id: "{person1_id}" }})
            MERGE (p2:Person {{ id: "{person2_id}" }})
            MERGE (p1)-[{relationship}]->(p2)
            """
            session.run(query)

# 关闭Neo4j驱动
driver.close()
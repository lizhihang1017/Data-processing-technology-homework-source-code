import pandas as pd
from neo4j import GraphDatabase

# 连接到 Neo4j 数据库
uri = "bolt://localhost:7687"  # 数据库地址
username = "neo4j"  # Neo4j 用户名
password = "不告诉你"  # Neo4j 密码
db_name = "test"  # 指定数据库名称

# 创建 Neo4j 驱动
driver = GraphDatabase.driver(uri, auth=(username, password))


def import_data_to_neo4j(csv_file):
    with driver.session(database=db_name) as session:
        # 读取 CSV 文件
        edges_df = pd.read_csv(csv_file)

        # 导入每一条边
        for index, row in edges_df.iterrows():
            source = row['person1_id']
            target = row['person2_id']
            relation_type = row['relation_type']

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
            MERGE (p1:Person {{ id: "{source}" }})
            MERGE (p2:Person {{ id: "{target}" }})
            MERGE (p1)-[{relationship}]->(p2)
            """
            session.run(query)


# 执行数据导入
csv_file_path = 'largest_family_ancestry_edges.csv'  # 指定你的 CSV 文件路径
import_data_to_neo4j(csv_file_path)

# 关闭 Neo4j 驱动
driver.close()

print("数据导入完成！")

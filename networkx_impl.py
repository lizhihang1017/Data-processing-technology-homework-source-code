import networkx as nx
import itertools

'''
查询最长路径
'''

# 创建一个空的无向图
G = nx.Graph()

# 读取数据文件
with open('testdata.txt', 'r') as file:
    lines = file.readlines()

# 解析每一行数据并构建图
for line in lines:
    parts = line.strip().split()
    if len(parts) >= 4:
        person1_id = int(parts[0])
        person2_id = int(parts[1])
        relation_type = parts[-1]

        # 添加边并设置关系类型作为边的属性
        G.add_edge(person1_id, person2_id, type=relation_type)

# 计算每个节点的度
degrees = dict(G.degree())

# 找到度最大的节点
# max_degree_node = max(degrees, key=degrees.get)
# max_degree = degrees[max_degree_node]
#
# print(f"度最大的节点是: {max_degree_node}，度数为: {max_degree}")


def find_longest_path(graph):
    longest_path = []
    max_length = 0

    # 遍历所有节点对
    for start_node, end_node in itertools.combinations(graph.nodes(), 2):
        try:
            path = nx.shortest_path(graph, source=start_node, target=end_node)
            path_length = len(path)

            if path_length > max_length:
                max_length = path_length
                longest_path = path
                print(f"找到新的最长路径：长度为 {max_length}，路径为 {path}")

        except nx.NetworkXNoPath:
            continue

    return longest_path, max_length


# 查找最长路径
longest_path, max_length = find_longest_path(G)
print(f"最长路径长度为: {max_length}")
print(f"路径为: {longest_path}")
import networkx as nx
import time

'''
通过动态规划结合拓扑排序计算有向图中的最长路径。
首先对图进行拓扑排序，以确保节点按依赖关系顺序处理。算法将每个节点的最长路径长度初始化为0，并记录其前驱节点。
随后，依次遍历排序后的节点，逐步更新每个后继节点的最长路径长度，确保始终保持路径最大。
最后，通过选择路径长度最大的终点，回溯前驱节点还原出最长路径，并记录其长度。
'''


# 创建一个空的有向图
G = nx.DiGraph()

print("开始读取数据文件并构建图...")
# 读取数据文件
with open('testdata.txt', 'r') as file:
    lines = file.readlines()

# 解析每一行数据并构建图
for line in lines:
    parts = line.strip().split()
    if len(parts) >= 4:
        person1_id = str(parts[0])  # 确保ID为字符串
        person2_id = str(parts[1])  # 确保ID为字符串
        relation_type = parts[-1]

        # 添加边并设置关系类型作为边的属性
        G.add_edge(person1_id, person2_id, type=relation_type)

print("图构建完成！")

# 环检测
if nx.is_directed_acyclic_graph(G):
    print("图中无环，开始计算最长路径...")
else:
    print("图中存在环，无法计算拓扑排序。请检查数据文件！")
    exit(1)

# 定义最长路径保存文件的路径
output_file = "longest_path.txt"

def save_longest_path(path, length):
    """实时保存最长路径和长度到本地文件."""
    with open(output_file, "w") as f:
        f.write(f"最长路径长度: {length}\n")
        f.write("路径: " + str(path) + "\n")

def find_longest_path(graph):
    print("开始计算最长路径...")

    # 拓扑排序
    topological_order = list(nx.topological_sort(graph))

    # 初始化最长路径和前驱节点字典
    longest_path = {node: 0 for node in graph.nodes}
    predecessor = {node: None for node in graph.nodes}

    # 动态规划计算最长路径
    for node in topological_order:
        for predecessor_node in graph.predecessors(node):
            if longest_path[predecessor_node] + 1 > longest_path[node]:
                longest_path[node] = longest_path[predecessor_node] + 1
                predecessor[node] = predecessor_node

    # 找到最长路径的终点
    end_node = max(longest_path, key=longest_path.get)
    max_length = longest_path[end_node]

    # 回溯找到最长路径
    path = []
    current_node = end_node
    while current_node is not None:
        path.append(current_node)
        current_node = predecessor[current_node]

    # 反转路径以获得正确的顺序
    path = path[::-1]

    print(f"找到最长路径：长度为 {max_length}，路径为 {path}")
    save_longest_path(path, max_length)

    return path, max_length

# 记录程序开始时间
start_time = time.time()
print("程序开始执行...")

# 查找最长路径
longest_path, max_length = find_longest_path(G)

# 计算并显示总运行时间
end_time = time.time()
total_time = end_time - start_time
print(f"程序总运行时间: {total_time:.2f} 秒")

print(f"最终最长路径长度为: {max_length}")
print(f"路径为: {longest_path}")
print("程序执行完毕。")
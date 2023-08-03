import dgl
import torch as th
import type_judge


# 根据triples统计节点类型和下标
# output: node_type_dic{node_type:dic{node:index}}
def gene_graph_node_dic(triples: list):
    graph_node_dic = {
        "未知": {},
        "空": {"null": 0}
    }
    for triple in triples:
        e1, e2 = triple[0], triple[2]
        e1_type, e2_type = type_judge.typejudge(triple)
        # 添加 e1node
        if e1_type not in graph_node_dic.keys():
            graph_node_dic.update({
                e1_type: {e1: 0}
            })
        else:
            e1_type_dic = graph_node_dic[e1_type]
            if e1 not in e1_type_dic.keys():
                e1_type_dic.update({
                    e1: len(e1_type_dic)
                })
        # 添加 e2node
        if e2_type not in graph_node_dic.keys():
            graph_node_dic.update({
                e2_type: {e2: 0}
            })
        else:
            e2_type_dic = graph_node_dic[e2_type]
            if e2 not in e2_type_dic.keys():
                e2_type_dic.update({
                    e2: len(e2_type_dic)
                })
    return graph_node_dic


# 根据单个triple更新graph_dic
def gene_graph_dic(graph_dic: dict, triple: tuple, graph_node_dic: dict):
    # 从graph_node_dic里取index
    e1, r, e2 = triple
    e1_type, e2_type = type_judge.typejudge(triple)
    e1_index = graph_node_dic[e1_type][e1]
    e2_index = graph_node_dic[e2_type][e2]
    # graph_dic中不存在该种边类型，更新graph_dic并添加新边类型和对应边
    edge = (e1_type, r, e2_type)
    if edge not in graph_dic.keys():
        graph_dic.update({
            edge: (th.tensor([e1_index]), th.tensor([e2_index]))
        })
        return graph_dic
    # graph_dic中存在该种边类型，取出该边类型对应的u_v.tensor更新
    u_v_tensor = graph_dic.get(edge)
    u_tensor = u_v_tensor[0]
    v_tensor = u_v_tensor[1]
    u_list = u_tensor.tolist()
    v_list = v_tensor.tolist()
    u_list.append(e1_index)
    v_list.append(e2_index)
    u_v_tensor = (th.tensor(u_list), th.tensor(v_list))
    graph_dic[edge] = u_v_tensor
    return graph_dic


# 生成异构图
def gene_graph(graph_dic: dict):
    graph = dgl.heterograph(graph_dic)
    return graph

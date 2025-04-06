from .node import Node
from .link import Link
from nal.truth import TruthValue
from nal.TruthValueFunctions import Truth_abduction, Truth_comparison, Truth_induction, Truth_deduction
import numpy as np

class Layer:
    def __init__(self, n_nodes):
        self.nodes = [Node() for _ in range(n_nodes)]

    def fully_connect(self, higher_layer: 'Layer'):
        for node in self.nodes:
            for other_node in higher_layer.nodes:
                node.connect_to(other_node)

    def clean(self):
        for node in self.nodes:
            node.truth_value.set_fc(0.0, 0.0)
            node.truth_value_back.set_fc(0.0, 0.0)


    def forward(self):
        for lower_node in self.nodes:
            for link in lower_node.higher_links:
                higher_node = link.higher_node
                truthv1 = link.truth_value
                truthv2 = lower_node.truth_value
                # truthv3 = Truth_abduction(truthv1, truthv2)
                truthv3 = Truth_comparison(truthv1, truthv2)
                higher_node.truth_value.revise(truthv3)

    def backprop(self):
        for higher_node in self.nodes:
            for link in higher_node.lower_links:
                lower_node = link.lower_node
                # deduction
                truthv1 = link.truth_value
                truthv2 = higher_node.truth_value_back
                truthv3 = Truth_deduction(truthv1, truthv2)
                lower_node.truth_value_back.revise(truthv3)
                # induction
                truthv1 = lower_node.truth_value
                truthv2 = higher_node.truth_value_back
                truthv3 = Truth_induction(truthv1, truthv2)
                link.truth_value.revise(truthv3)
                


    def set_weights(self, weights: list[list[tuple[float, float]]]):
        """
        weights: shape=(n_nodes1, n_nodes2, 2); weights[i, j] is the truth-value of the link from node i to node j 
        """
        for i, lower_node in enumerate(self.nodes):
            weights_i = weights[i]
            for j, link in enumerate(lower_node.higher_links):
                f, c = weights_i[j]
                link.truth_value.set_fc(f, c)
    
    def input(self, truth_values: list[tuple[float, float]]):
        """
        truth_values: shape=(n_nodes, 2); truth_values[i] is the truth-value of node i
        """
        for i, node in enumerate(self.nodes):
            f, c = truth_values[i]
            node.truth_value.revise_fc(f, c)
    
    def input_back(self, truth_values: list[tuple[float, float]]):
        """
        truth_values: shape=(n_nodes, 2); truth_values[i] is the truth-value of node i
        """
        for i, node in enumerate(self.nodes):
            f, c = truth_values[i]
            node.truth_value_back.revise_fc(f, c)
                

def visualize_layers(layers: list[Layer], show_truthvalue=False, node_size=700):
    import matplotlib.pyplot as plt
    import networkx as nx

    G = nx.DiGraph()

    # 添加节点时设置层属性（这里用整数表示层次）
    for i, layer in enumerate(layers):
        for node in layer.nodes:
            attr = {'layer': i}
            if show_truthvalue:
                attr['truth_value'] = str(node.truth_value)
            G.add_node(id(node), **attr)

    # 添加边
    for layer in layers:
        for node in layer.nodes:
            for link in node.higher_links:
                attr = {}
                if show_truthvalue:
                    attr = {'truth_value': str(link.truth_value)}
                G.add_edge(id(link.lower_node), id(link.higher_node), **attr)

    # 使用multipartite_layout，根据节点的'layer'属性来布局
    pos = nx.multipartite_layout(G, subset_key="layer")

    # 绘制图形
    nx.draw(
        G, pos,
        with_labels=False,
        node_size=node_size,
        node_color='lightblue',
        font_size=10,
        font_weight='bold',
        arrows=True
    )
    if show_truthvalue:
        nx.draw_networkx_labels(G, pos, labels={n: f"{data['truth_value']}" for n, data in G.nodes(data=True)})
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): data['truth_value'] for u, v, data in G.edges(data=True)})
    plt.show()

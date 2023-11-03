"""
Define class SynthTree,
which is a tree of SynthNodes that represent the chemical synthesis described in a document.
"""

import os
from typing import Optional

import networkx as nx
from bigtree import (
    Node,
    copy_nodes_from_tree_to_tree,
    findall,
    nested_dict_to_tree,
    tree_to_dataframe,
)
from pandas import DataFrame

from .synthdoc import SynthDocument


class SynthTree(SynthDocument):
    """Extend SynthDocument to represent reaction tree."""

    def __init__(self, doc_src: str, api_key: Optional[str] = None) -> None:
        """Initialize a SynthTree object."""
        super(SynthTree, self).__init__(doc_src, api_key)

        self.extract_rss()

        self.trees = self.dictionaries2trees(self.rxn_setups)
        print(self.trees)
        # Merge trees to create bigger structures
        self.merged_trees = self.merge_trees(self.trees)
        self.networks = self.bigtrees_to_networks(
            self.merged_trees
        )  # Convert trees to networkx objects

    def dictionaries2trees(
        self, dict_list: list, name_key: str = "reference_key", child_key: str = "children"
    ):
        """
        Converts a list of dictionaries representing tree-like structures
        into a list of bigtree Node objects.

        Parameters:
            dict_list (list): A list of dictionaries representing tree-like structures.

        Returns:
            tree_list (list): A list of trees converted from the input dictionaries.
        """

        tree_list = []

        # Convert each dictionary to a tree
        for dictionary in dict_list:
            if name_key not in dictionary.keys() or child_key not in dictionary.keys():
                raise KeyError(
                    f"Expected name_key '{name_key}' or child_key '{child_key}' not in dictionary {dictionary}"
                )

            print("@@@@@@@@@@@|")
            print(dictionary)
            print(name_key)
            print(child_key)
            print("@@@@@@@@@@@|")

            new_tree = nested_dict_to_tree(
                node_attrs=dictionary, name_key=name_key, child_key=child_key
            )
            tree_list.append(new_tree)

        return tree_list

    def merge_trees(self, tree_list: list):
        """
        Merges a list of trees represented as bigtree Node objects.

        Parameters:
            tree_list (list): A list of trees represented as bigtree Node objects.

        Returns:
            merged + solo_nodes (list): A list of merged trees and solo nodes.
        """

        # If the input tree list is empty, return an empty list
        if not tree_list:
            return []

        if all(isinstance(t, Node) for t in tree_list):
            # Separate the trees with no children (solo nodes)
            solo_nodes = [t for t in tree_list if not t.children]
            tree_structs = [t for t in tree_list if t.children]

            # Merge trees with children together
            merged = self.__merge_trees_helper(tree_structs, results=[])

            # Combine lists of merged trees and solo nodes
            return merged + solo_nodes

        else:
            raise ValueError("Input list is not a list of only bigtree Node objects.")

    def bigtrees_to_networks(
        self,
        tree_list: list,
        name_col: str = "reference_key",
        parent_col: str = "parent",
        all_attrs: bool = True,
    ):
        """
        Converts a list of bigtree Node objects to a list of networkx DiGraph objects.
        Each tree is first converted to a dataframe and then transformed into a directed graph.
        Optionally, it can include all attributes for each node as node attributes in the graph.

        Parameters:
            tree_list (list):
                A list of trees represented as dictionaries or dataframes.
            name_col (str):
                The name to be assigned to the column containing the node name in each tree. Default is 'reference_num'.
            parent_col (str):
                The name to be assigned to the column containing the parent node name in each tree. Default is 'parent'.
            all_attrs (bool):
                A flag indicating whether to include all attributes for each node. Default is True.

        Returns:
            networks (list): A list of networkx DiGraph objects representing the input trees.
        """

        if not tree_list:
            return []

        if all(isinstance(t, Node) for t in tree_list):
            networks = []

            # Convert each tree to a dataframe and then to a directed graph
            for tree in tree_list:
                df = tree_to_dataframe(
                    tree, name_col=name_col, parent_col=parent_col, all_attrs=all_attrs
                )
                graph = self._df_to_graph(df, node_name_col=name_col, parent_col=parent_col)

                networks.append(graph)

            return networks

        else:
            raise ValueError("Input list is not a list of only bigtree Node objects.")

    def __merge_trees_helper(self, tree_list: list, results: list):
        """
        Helper function to merge a list of trees represented as bigtree Node objects.

        Parameters:
            tree_list (list): A list of trees represented as bigtree Node objects to be merged.
            results (list): A list to store the resulting merged trees.

        Returns:
            results (list): A list of merged trees accumulated during the tail-recursive process.
        """

        # Use first tree as a base to see what other trees can merge into it
        final_tree = tree_list.pop(0)

        # List to append trees that didn't merge with final_tree
        retry_list = []

        for tree in tree_list:
            # Check if a merge tree -> final_tree is possible
            merge_1 = self.__find_and_copy_to_tree(final_tree, tree)

            if merge_1[0] == 0:
                # If it was, final_tree is now the bigger resulting tree from the merge
                final_tree = merge_1[1]

            else:
                # If it wasn't, check if merge final_tree -> tree is possible
                merge_2 = self.__find_and_copy_to_tree(tree, final_tree)

                if merge_2[0] == 0:
                    # If it was, final_tree is now the bigger resulting tree from the merge
                    final_tree = merge_2[1]
                else:
                    # If it wasn't, tree has no common nodes with final_tree so it will go into the retry_list
                    retry_list.append(tree)

        # Add the resulting merged tree to results
        results.append(final_tree)

        # If the retry_list is not empty, rerun the function. The results list will keep growing
        if retry_list:
            self.__merge_trees_helper(tree_list=retry_list, results=results)

        return results

    def __find_and_copy_to_tree(self, big_tree: Node, small_tree: Node):
        """
        Find nodes with the same name as 'small_tree' in 'big_tree'
        and copy the 'small_tree' into the first node found.

        Parameters:
            big_tree (Node): The target tree to search for nodes with the same name as small_tree.
            small_tree (Node): The tree whose nodes are searched and copied into big_tree.

        Returns:
            (int, Node): A tuple containing:
            - 0: If nodes with the same name were found in big_tree and successfully merged.
            - 1: If there were no nodes with the same name found in big_tree.
            - big_tree: The modified 'big_tree' after the merge operation.
        """

        # Find all nodes in 'big_tree' that have the same name as 'small_tree'
        search = findall(big_tree, lambda node: node.name == small_tree.name)

        if not search:
            # If there are no nodes with the name 'small_tree' in 'big_tree', return 1 and the original 'big_tree'
            return 1, big_tree
        else:
            # If nodes with the name 'small_tree' were found in 'big_tree'
            # Merge 'small_tree' into the first node with the same name in 'big_tree' (will not merge to other nodes)
            dest_path = search[0].path_name
            orig_path = small_tree.path_name

            # Merge 'small_tree' into 'big_tree'
            # Obtained from Tips and Tricks page in bigtree documentation
            copy_nodes_from_tree_to_tree(
                from_tree=small_tree,
                to_tree=big_tree,
                from_paths=[orig_path],
                to_paths=[dest_path],
                overriding=True,
            )

            # Return 0 and the new merged 'big_tree'
            return 0, big_tree

    def _df_to_graph(
        self,
        df: DataFrame,
        node_name_col: str = "reference_num",
        parent_col: str = "parent",
        cols_to_ignore: list = ["path"],
    ):
        """
        Converts a dataframe representing a tree to a networkx DiGraph object.
        The dataframe should have columns for node names, parent node names,
        and any additional attributes for each node.

        Parameters:
            df (pandas.DataFrame):
                The input dataframe representing a tree.
            node_name_col (str):
                The name of the column containing the node names in the dataframe. Default is 'reference_num'.
            parent_col (str):
                The name of the column containing the parent node names in the dataframe. Default is 'parent'.
            cols_to_ignore (list):
                A list of column names to ignore while adding attributes to the nodes. Default is ['path'].

        Returns:
            graph (networkx.DiGraph): A directed graph representing the input dataframe as a tree.
        """

        if df.empty:
            raise ValueError("Database is empty")

        # Check cols_to_ignore only has strings
        if not all(isinstance(elem, str) for elem in cols_to_ignore):
            raise ValueError(
                "The list 'cols_to_ignore' must only contain strings corresponding to columns in the DataFrame df"
            )

        # Check all elems in cols_to_ignore are valid column names in the dataframe
        for elem in cols_to_ignore:
            if elem not in list(df.columns):
                raise ValueError(
                    f"String '{elem}' in 'cols_to_ignore' does not correspond to a valid column in the dataframe"
                )

        # Create DiGraph object
        graph = nx.DiGraph()

        # Iterate over each row in the dataframe to add nodes and edges to the graph
        for _, row in df.iterrows():
            node_name = row[node_name_col]
            parent_node = row[parent_col]

            # Create a unique node identifier by combining reference_num and parent_node
            unique_node_name = f"{node_name}_[{parent_node}]"

            parent_unique_name = None

            if parent_node is not None:
                # Get parent node unique name
                parent_row = df.loc[df[node_name_col] == parent_node]
                if not parent_row.empty:
                    parent_unique_name = (
                        f"{parent_row.iloc[0][node_name_col]}_[{parent_row.iloc[0][parent_col]}]"
                    )

            # Add node
            graph.add_node(unique_node_name)

            # Add attributes to node for each column
            # (excluding the node_name_col, the parent_col, and anything in 'cols_to_ignore')
            for column, value in row.drop([node_name_col, parent_col] + cols_to_ignore).items():
                graph.nodes[unique_node_name][column] = value

            # Add edges except to root node and avoiding edges that point to self
            if parent_unique_name is not None and parent_unique_name != unique_node_name:
                graph.add_edge(parent_unique_name, unique_node_name)

        return graph

    def images_from_graphs(
        self,
        networks: list,
        path: str = "./network_images",
        default_img_name: str = "graph",
        prog: str = "dot",
        node_color1: str = "#fc60ac",
        node_color2: str = "#fcb6d8",
        split_label: bool = True,
        split_char: str = "_",
    ):
        """
        Save images of networkx DiGraph objects as PNG files.

        Parameters:
            networks (list): A list of networkx DiGraph objects to be saved as images.
            path (str): The path to the directory where images will be saved. Default is "./network_images".
            default_img_name (str): The default base name for the saved images. Default is "graph".
            prog (str): The graph layout program for pygraphviz. Default is "dot".

        Returns:
            None: The function saves images of the input graphs to the specified directory.
        """

        if all(isinstance(t, nx.classes.digraph.DiGraph) for t in networks):
            if not os.path.exists(path):
                os.makedirs(path)

            for i, network in enumerate(networks):
                file_name = f"{default_img_name}{str(i)}.png"
                file_path = os.path.join(path, file_name)

                if os.path.exists(file_path):
                    os.remove(file_path)

                py_net = nx.nx_agraph.to_agraph(network)
                py_net.node_attr["style"] = "filled"

                for node in py_net:
                    if split_label:
                        node.attr["label"] = node.split(split_char, 1)[0]

                    if network.out_degree(node) != 0:
                        node.attr["fillcolor"] = node_color1
                    else:
                        node.attr["fillcolor"] = node_color2

                py_net.layout(prog=prog)
                py_net.draw(file_path)

        else:
            raise ValueError("Input list must only contain DiGraph networkx objects")

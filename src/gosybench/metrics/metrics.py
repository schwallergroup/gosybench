"""Metrics for quality of extraction."""



# Similar thing, but with pruned trees paths (test only backbone)


def get_paths(G):
    paths = []
    for n0 in G.nodes:
        for n1 in G.nodes:
            if n0 != n1:
                if nx.has_path(G, n0, n1):
                    ps = nx.all_simple_paths(G, source=n0, target=n1)
                    paths += list(ps)
    return paths


def prune(G):
    """Drop all nodes with outdeg==0."""
    pruned = G.copy()
    for node in G.nodes:
        if G.out_degree(node) == 0:
            pruned.remove_node(node)
    return pruned


def compare_path_exact_0(G, gt_G):
    """How many paths in pruned-G are also in pruned-gt_G"""
    quant = []
    subgraphs = get_paths(G)
    for path in subgraphs:
        if len(path) > 1:
            sg = G.subgraph(path)
            v = subgraph_in_gt_exact(sg, gt_G)
            quant.append(v)

    return (sum(quant) + 1) / (len(quant) + 1)


def compare_path_exact_pruned(gt_G, G):
    pG = prune(G)
    pgt_G = prune(gt_G)

    # gt_G in G
    c0 = compare_path_exact_0(pgt_G, pG)
    # G in gt_G
    c1 = compare_path_exact_0(pG, pgt_G)
    return c0, c1


# Similar thing, but with paths (testing more long-range structure)


def get_paths(G):
    paths = []
    for n0 in G.nodes:
        for n1 in G.nodes:
            if n0 != n1:
                if nx.has_path(G, n0, n1):
                    ps = nx.all_simple_paths(G, source=n0, target=n1)
                    paths += list(ps)
    return paths


def compare_path_exact_0(G, gt_G):
    """How many paths in G are also in gt_G"""
    quant = []
    subgraphs = get_paths(G)
    for path in subgraphs:
        if len(path) > 1:
            sg = G.subgraph(path)
            v = subgraph_in_gt_exact(sg, gt_G)
            quant.append(v)
    return (sum(quant) + 1) / (len(quant) + 1)


def compare_path_exact(gt_G, G):
    # gt_G in G
    c0 = compare_path_exact_0(gt_G, G)
    # G in gt_G
    c1 = compare_path_exact_0(G, gt_G)
    return c0, c1



def compare_porder_0(G, gt_G):
    quant = []
    subgraphs = get_paths(G)
    for path in subgraphs:
        if len(path) > 2:
            sg = POSet(path=G.subgraph(path))
            gt_sg = POSet(path=gt_G.subgraph(path))
            quant.append(sg.iso(gt_sg))

    return (sum(quant) + 1) / (len(quant) + 1)


def compare_porder(gt_G, G):
    c0 = compare_porder_0(gt_G, G)
    c1 = compare_porder_0(G, gt_G)
    return c0, c1


# loc = compare_porder(gt, og)
# pat = compare_path_exact(gt, og)
# prun = compare_path_exact_pruned(gt, og)


#     df.append(
#         {
#             "paper": paper,
#             "model": model,
#             "method": method,
#             "si_select": si_select,
#             "path_sim_in": pat[0],
#             "path_sim_out": pat[1],
#             "local_sim_in": loc[0],
#             "local_sim_out": loc[1],
#             "ploc_sim_in": prun[0],
#             "ploc_sim_out": prun[1],
#         }
#     )


# for m in [
#     "local_sim_in",
#     "local_sim_out",
#     "path_sim_in",
#     "path_sim_out",
#     "ploc_sim_in",
#     "ploc_sim_out",
# ]:
#     make_plot(m)
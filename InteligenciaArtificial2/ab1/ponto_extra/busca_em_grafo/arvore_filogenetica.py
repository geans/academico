from pandas import read_csv
from os import system
import argparse


def like_entropy(group, c_features):
    if len(group) == 0:
        return []
    max_many = 0
    feature = []
    for f in c_features:
        have = group[group[f] == 1]
        no_have = []#group[group[f] == 0]
        x = max(len(no_have), len(have))
        if x > max_many:
            max_many = x
            feature = [f]
        elif x == max_many:
            feature += [f]
    return feature

    
def divide_conquer(group, c_features, tree, ancestor_count):
    dividing_feature = like_entropy(group, c_features)
    if dividing_feature == []:
        if len(list(group['Especie'])) == 1:
            return list(group['Especie'])[0], tree, ancestor_count
        else:
            return list(group['Especie']), tree, ancestor_count
    f = dividing_feature[0]
    group1 = group[group[f] == 1]
    group2 = group[group[f] == 0]
    
    last_features = list(c_features)
    last_features.remove(f)

    if 0 in [len(group1), len(group2)]:
        if len(group1) == 0:
            ancestor, tree, ancestor_count = divide_conquer(group2, last_features, tree, ancestor_count)
        else:
            ancestor, tree, ancestor_count = divide_conquer(group1, last_features, tree, ancestor_count)
        ancestor_count += 1
        ancestor_name = 'ancestor_{}'.format(ancestor_count)
        tree[ancestor_name] = [ancestor, f]
    else:
        # ca = common ancestor
        if len(group1) == 1:
            ca1 = list(group1['Especie'])[0]
        else:
            ca1, tree, ancestor_count = divide_conquer(group1, last_features, tree, ancestor_count)
        if len(group2) == 1:
            ca2 = list(group2['Especie'])[0]
        else:
            ca2, tree, ancestor_count = divide_conquer(group2, last_features, tree, ancestor_count)

        ancestor_count += 1
        ancestor_name = 'ancestor_{}'.format(ancestor_count)
        tree[ancestor_name] = [ca1, ca2, f]
    return ancestor_name, tree, ancestor_count


def build_graphviz(node, tree):
    try:
        soon, feature = tree[node][0], tree[node][-1]
    except Exception:
        return ''
    branch = build_graphviz(soon, tree)
    graphviz = branch + '\t{} -> {} [label="{}"]\n'.format(node, soon, feature)
    other_soon = tree[node][1:-1]
    for soon in other_soon:
        branch = build_graphviz(soon, tree)
        graphviz += branch + '\t{} -> {}\n'.format(node, soon)
    return graphviz

if __name__ == '__main__':
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--csv", required=True, help="Path to input CSV file")
    ap.add_argument("-o", "--out", default='out', help="Name to output file")
    args = vars(ap.parse_args())
    input_filename = args['csv']
    output_filename = args['out']
    
    tree = {}
    ancestor_count = 0
    group = read_csv(input_filename)
    c_features = list(group)[1:]
    root, tree, ancestor_count = divide_conquer(group, c_features, tree, ancestor_count)

    graphviz = 'digraph FileGenetica {\n'
    tree_graph = build_graphviz(root, tree)
    graphviz += tree_graph + '}'
    
    file = open(output_filename + '.dot', 'w')
    file.write(graphviz)
    file.close()
    
    try:
        system('dot -Tpdf {0}.dot -o {0}.pdf'.format(output_filename))
        print('Out to PDF')
    except Exception:
        print(graphviz)
        
def print_tree(tree, prefix=""):
    if not isinstance(tree, list):
        print(prefix + str(tree[0]))
        return
    for sub in tree:
        print(prefix + str(sub[0]))
        print_tree(sub[1], prefix="  "+prefix)
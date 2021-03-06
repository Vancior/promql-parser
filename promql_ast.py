import io


class ASTNode:
    def __new__(cls, grammar_type):
        if grammar_type == 'label_selector':
            return super().__new__(LabelSelector)
        return super().__new__(ASTNode)

    def __init__(self, grammar_type):
        self.grammar_type = grammar_type
        self.children = []

    def __str__(self):
        sio = io.StringIO()
        for child in self.children:
            if isinstance(child, ASTNode):
                sio.write(str(child))
            elif isinstance(child, str):
                sio.write(child)
            else:
                raise RuntimeError('unknown ast node')
        s = sio.getvalue()
        sio.close()
        return s


class LabelSelector(ASTNode):
    def __str__(self):
        return ','.join([k + '=' + v + '' for k, v in self.children])


def recur_print(root: ASTNode):
    for child in root.children:
        if isinstance(child, ASTNode):
            recur_print(child)
        elif isinstance(child, str):
            print(child)
        else:
            raise RuntimeError('unknown ast node')


def recur_add_label(root: ASTNode, label, value):
    if isinstance(root, LabelSelector):
        root.children.append((label, value))
    for child in root.children:
        if isinstance(child, ASTNode):
            recur_add_label(child, label, value)

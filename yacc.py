import ply.yacc as yacc

from lexer import tokens
from promql_ast import ASTNode


def make_ast_node(p, grammar_type: str):
    node = ASTNode(grammar_type)
    for i in range(1, len(p)):
        node.children.append(p[i])
    p[0] = node


def p_expression_binary(p):
    """expression : expression FST_OP term
                | term"""
    make_ast_node(p, 'expression')


def p_term_binary(p):
    """term : term SEC_OP factor
                | factor"""
    make_ast_node(p, 'term')


def p_factor(p):
    """factor : NUMBER
                | STRING
                | metric
                | aggr
                | func
                | LEFT_PAREN expression RIGHT_PAREN"""
    make_ast_node(p, 'factor')


def p_metric(p):
    """metric : metric_inner
                | metric_inner LEFT_BRACKET TIME RIGHT_BRACKET"""
    make_ast_node(p, 'metric')


def p_metric_inner(p):
    """metric_inner : IDENTIFIER
                | IDENTIFIER LEFT_BRACE label_selector RIGHT_BRACE"""
    make_ast_node(p, 'metric_inner')
    if len(p) == 2:
        p[0].children.append('{')
        p[0].children.append(ASTNode('label_selector'))
        p[0].children.append('}')


def p_label_selector(p):
    """label_selector : IDENTIFIER EQ STRING
                | IDENTIFIER EQ STRING COMMA label_selector"""
    if len(p) == 4:
        node = ASTNode('label_selector')
        node.children.append((p[1], p[3]))
        p[0] = node
    else:
        assert isinstance(p[5], ASTNode)
        p[0] = p[5]
        p[0].children.append((p[1], p[3]))


def p_aggr(p):
    """aggr : AGGR_OP LEFT_PAREN parameter RIGHT_PAREN
                | AGGR_OP LEFT_PAREN parameter RIGHT_PAREN AGGR_KEY LEFT_PAREN label_list RIGHT_PAREN"""
    make_ast_node(p, 'aggr')


def p_parameter(p):
    """parameter : expression
                | expression COMMA parameter"""
    if len(p) == 2:
        make_ast_node(p, 'parameter')
    else:
        assert isinstance(p[3], ASTNode)
        p[0] = p[3]
        for i in range(2, 0, -1):
            p[0].children.insert(0, p[i])


def p_label_list(p):
    """label_list : IDENTIFIER
                | IDENTIFIER COMMA label_list"""
    if len(p) == 2:
        make_ast_node(p, 'label_list')
    else:
        assert isinstance(p[3], ASTNode)
        p[0] = p[3]
        for i in range(2, 0, -1):
            p[0].children.insert(0, p[i])


def p_func(p):
    """func : FUNC LEFT_PAREN parameter RIGHT_PAREN"""
    make_ast_node(p, 'func')


def p_error(p):
    print("Syntax error in input!")
    print(p)


parser = yacc.yacc()

if __name__ == '__main__':
    s = '12*(123-1)'
    result = parser.parse(s)
    # print(result)

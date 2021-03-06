"""
identifier
number
time
string
binary_op
unary_op

expression

metric = id\{label_selector\}\[range_selector\]

aggr_exp = aggr_op [without | by \(label_list\)] \( [parameter\,] expression\)
# aggr_exp = aggr_op \( [parameter\,] expression\) [without | by \(label_list\)]

function_call = id\(expression\)

label_selector = id \= string (\,id \= string)*
range_selector = time
label_list = id (\,id)*
parameter = expression

unary_item

item = number | string | expression |

expression = expression + term | expression - term | term
term = term * factor | term / factor | factor
factor = number | (expression)

"""

from ply import lex

reserved = {
    'without': 'AGGR_KEY',
    'by': 'AGGR_KEY',
    'sum': 'AGGR_OP',
    'min': 'AGGR_OP',
    'max': 'AGGR_OP',
    'avg': 'AGGR_OP',
    'group': 'AGGR_OP',
    'stddev': 'AGGR_OP',
    'stdvar': 'AGGR_OP',
    'count': 'AGGR_OP',
    'count_values': 'AGGR_OP',
    'bottomk': 'AGGR_OP',
    'topk': 'AGGR_OP',
    'quantile': 'AGGR_OP',
    'rate': 'FUNC',
    'irate': 'FUNC',
}

tokens = (
    'NUMBER',
    'TIME',
    'IDENTIFIER',
    'STRING',
    'FST_OP',
    'SEC_OP',
    'EQ',
    'COMMA',
    'LEFT_PAREN',
    'RIGHT_PAREN',
    'LEFT_BRACE',
    'RIGHT_BRACE',
    'LEFT_BRACKET',
    'RIGHT_BRACKET',
    'AGGR_KEY',
    'AGGR_OP',
    'FUNC'
)

t_NUMBER = r'(([1-9][0-9]*)|0)(\.[0-9]*)?'
t_TIME = r'(([1-9][0-9]*)[s|m|h|d|w|y])+'
t_STRING = r'\"(([^\\](?!\")).)*.?((?<!\\)\")'
t_FST_OP = r'\+|\-'
t_SEC_OP = r'\*|\/'
t_EQ = '='
t_COMMA = ','
t_LEFT_PAREN = r'\('
t_RIGHT_PAREN = r'\)'
t_LEFT_BRACE = r'\{'
t_RIGHT_BRACE = r'\}'
t_LEFT_BRACKET = r'\['
t_RIGHT_BRACKET = r'\]'

t_ignore = ' \t'


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


def t_error(t):
    print("error in", t)
    exit()


lexer = lex.lex()

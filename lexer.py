import sys
from ply import lex

tokens = ['TEXT', 'BEGIN', 'END',
	'STRING', 'IDENTIFIER', 'CONCAT', 'SEMICOLON', 'ASSIGN',
	'EQUALS']
keywords = ('PRINT', 'FOR', 'IN', 'DO', 'ENDFOR', 'IF', 'ENDIF', 'ELSE')
tokens.extend(keywords) #idea from http://stackoverflow.com/a/5028233
states = (('code', 'exclusive'), )

def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	#hack
	t.type = 'TEXT'
	return t
t_TEXT = r'[^{]+'
def t_BEGIN(t):
	'{{'
	t.lexer.begin('code')
	return t
def t_code_END(t):
	'}}'
	t.lexer.begin('INITIAL')
	return t
def t_error(t):
	#this should never run!
	assert(False)

t_code_ignore = ' \t'
def t_code_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	pass
t_code_CONCAT = r'\.'
t_code_SEMICOLON = ';'
t_code_ASSIGN = ':='
t_code_EQUALS = '='
def t_code_IDENTIFIER(t):
	'[a-zA-Z0-9_]+'
	u = t.value.upper()
	if u in keywords:
		t.type = u
	return t
def t_code_STRING(t):
	r"'([^']|\')+'"
	t.value = t.value[1:-1].replace(r"\'", "'")
	#TODO regex replace for at least unescaped \n and \t
	return t
def t_code_error(t):
	print >>sys.stdout, "Illegal character:", t.value[0]
	t.lexer.skip(1)

lex = lex.lex()
if __name__=="__main__":
	lex.input(sys.stdin.read())
	for token in lex:
		print token.type

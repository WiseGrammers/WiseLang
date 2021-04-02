# Imports
from sly import Lexer, Parser
import ast

# Lexer Class Start
class WiseLexer(Lexer):
	tokens = {
		NAAM, NUMBER, STRING,
		PRINT, INPUT, DECLARE,
		# PASS, BREAK, IF, ELIF,
		# ELSE, LBRAC, RBRAC,
		PLUS, SUB, MUL,
		DIV, MOD, LPAREN,
		RPAREN, EQ, NE
	}


	# Ignored patterns
	ignore_newline = r'\n+'
	ignore_comment = r'//.*\n*'
	ignore = ' \t'

	literals = {
		'='
	}

	# Define tokens as regular expressions
	# (stored as raw strings)
	NAAM = r'[a-zA-Z_\$][a-zA-Z0-9_]*'
	STRING = r'\".*?\"'

	# NAAM["agar yeh"] = ELIF
	# NAAM["agar"] = IF
	# NAAM["chutiya"] = PASS
	NAAM["eww"] = PRINT
	NAAM["input"] = INPUT
	NAAM["WTF"] = DECLARE
	# NAAM["hatt"] = BREAK
	# NAAM["nahi toh"] = ELSE

	# Operators
	# LBRAC = r'\{'
	# RBRAC = r'\}'
	LPAREN = r'\('
	RPAREN = r'\)'
	EQ = r'=='
	NE = r'!='
	PLUS = r'\+'
	SUB = r'-'
	MUL = r'\*'
	DIV = r'/'
	MOD = r'%'

	# Number token
	@_(r'\d+')
	def NUMBER(self, t):
		# convert it into a python integer
		t.value = int(t.value) 
		return t

	@_(r'\".*?\"')
	def STRING(self, t):
		# un-escape escaped characters
		if len(t.value) > 0:
			t.value = ast.literal_eval(t.value)
		return t

	def ignore_newline(self, t):
		self.lineno += t.value.count('\n')

	# error handling
	def error(self, t):
		print(f"Error: line {self.lineno}:{self.index} Illegal character '%s'" % t.value[0])
		self.index += 1
		return t
# Lexer Class End

# Parser Class Start
class WiseParser(Parser):
	tokens = WiseLexer.tokens

	precedence = (
		('left', EQ, NE),
		('left', PLUS, SUB),
		('left', MUL, DIV),
		('left', MOD),
		('right', 'UMINUS'),
		('left', PRINT, INPUT)
	)

	@_('statements')
	def main(self, p):
		return ('main', p.statements)

	@_('statement')
	def statements(self,p):
		return ('statements', [p.statement])

	@_('statements statement')
	def statements(self,p):
		return ('statements', p.statements[1] + [p.statement])

	@_('PRINT statement')
	def statement(self, p):
		return ('print', p.statement)

	@_('INPUT statement')
	def statement(self, p):
		return ('input', p.statement)

	@_('expr')
	def statement(self, p):
		return ('expr', p.expr)

	@_('LPAREN expr RPAREN')
	def statement(self, p):
		return ('wrapped-expr', p.expr)

	@_('DECLARE NAAM "=" statement')
	def statement(self, p):
		return ('assign', p.NAAM, p.statement)

	@_('expr PLUS expr')
	def expr(self, p):
		return ('add', p.expr0, p.expr1)

	@_('expr SUB expr')
	def expr(self, p):
		return ('sub', p.expr0, p.expr1)

	@_('expr MUL expr')
	def expr(self, p):
		return ('mul', p.expr0, p.expr1)

	@_('expr DIV expr')
	def expr(self, p):
		return ('div', p.expr0, p.expr1)

	@_('expr MOD expr')
	def expr(self, p):
		return ('mod', p.expr0, p.expr1)

	@_('expr EQ expr')
	def expr(self, p):
		return ('eq', p.expr0, p.expr1)

	@_('expr NE expr')
	def expr(self, p):
		return ('not_eq', p.expr0, p.expr1)

	@_('SUB expr %prec UMINUS')
	def expr(self, p):
		return ('negate', p.expr)

	@_('NUMBER')
	def expr(self, p):
		return ('num', p.NUMBER)

	@_('STRING')
	def expr(self, p):
		return ('str', p.STRING)

	@_('NAAM')
	def expr(self, p):
		return ('var', p.NAAM)

	# @_('PASS')
	# def statement(self, p):
	# 	pass

	# @_('BREAK')
	# def statement(self, p):
	# 	return ('break', p.BREAK)

	# @_('IF condition LBRAC statement RBRAC [ ELIF expr LBRAC statement RBRAC ] [ ELSE LBRAC RBRAC ] ')
	# def statement(self, p):
	# 	return ('if_stmt', p.condition, ('branch', p.statement0, p.expr0, p.statement1, p.statement2))
# Parser Class End

# Executor Class Start
class Executor:

	def _NameError(self, name):
		return f"NameError: line {self.lineno}, Variable {name} is not defined"

	def _OperationError(self, operator, typeA, typeB=None):
		if typeB:
			return f"OperationError: line {self.lineno}, Unsupported operation: {operator} between types: {typeA} and {typeB}"
		return f"OperationError: line {self.lineno}, Unsupported operation: {operator} with type: {typeA}"

	def _DivisionByZeroError(self):
		return f"DivisionByZeroError: line {self.lineno}, cannot divide by zero"

	@staticmethod
	def _type(_obj):
		return str(type(_obj)).split("'")[1]

	def __init__(self, env, config):
		self.env = env
		self.conf = config
		self.lineno = 1

	def run(self, tree):
		if self.conf["DEBUG"]:
			print('[DEBUG]:', tree)

		try:
			rule = tree[0]
		except TypeError:
			return print('Exception: INTERNAL ERROR!!')

		if rule == 'main':
			self.run(tree[1])

		elif rule == 'statements':
			for i in tree[1]:
				self.run(i)
				self.lineno += 1

		elif rule == 'expr':
			val = self.run(tree[1])
			if val is None:
				return
			return val

		elif rule == 'assign':
			val = self.run(tree[2])
			if val is None: return

			self.env[tree[1]] = val
			return val

		elif rule in ('mul', 'div', 'add', 'sub', 'mod'):
			x = self.run(tree[1])
			y = self.run(tree[2])
			if x is None or y is None: return

			try:
				if rule == 'mul':
					op = '*'
					return x * y
				elif rule == 'div':
					op = '/'
					if y == 0:
						return print(self._DivisionByZeroError())
					return x / y
				elif rule == 'add':
					op = '+'
					return x + y
				elif rule == 'sub':
					op = '-'
					return x - y
				elif rule == 'mod':
					op = '%'
					return x % y
			except TypeError:
				return print(self._OperationError(op, self._type(x), self._type(y)))

		elif rule == 'eq':
			return self.run(tree[1]) == self.run(tree[2])
		elif rule == 'not_eq':
			return self.run(tree[1]) != self.run(tree[2])

		elif rule == 'negate':
			val = self.run(tree[1])
			if val is None:
				return
			try:
				return -val
			except TypeError:
				return print(self._OperationError('-', self._type(val)))

		elif rule in ('num', 'str'):
			return tree[1]

		elif rule == 'var':
			try:
				return self.env[tree[1]]
			except KeyError:
				return print(self._NameError(tree[1]))

		elif rule == 'wrapped-expr':
			val = self.run(tree[1])
			if val is None:
				return
			return val

		elif rule == 'print':
			val = self.run(tree[1])
			if val is None:
				return
			print(val)
			return val

		elif rule == 'input':
			val = self.run(tree[1])
			if val is None:
				return
			return input(val)

		else:
			return print("Exception: INTERNAL ERROR!!")
# Executor Class End
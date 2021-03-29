# Imports
from sly import Lexer
from sly import Parser

# Lexer Class Start
class BasicLexer(Lexer):
	tokens = { NAAM, NUMBER, STRING, PRINT}
	ignore = '\t '
	literals = { '=', '+', '-', '/', 
				'*', '(', ')', ',', ';'}
  
  
	# Define tokens as regular expressions
	# (stored as raw strings)
	NAAM = r'[a-zA-Z_][a-zA-Z0-9_]*'
	STRING = r'\".*?\"'
	NAAM["eww"] = PRINT
  
	# Number token
	@_(r'\d+')
	def NUMBER(self, t):
		
		# convert it into a python integer
		t.value = int(t.value) 
		return t

	# Comment token
	@_(r'//.*')
	def COMMENT(self, t):
		pass
  
	# Newline token(used only for showing
	# errors in new line)
	@_(r'\n+')
	def NEWLINE(self, t):
		self.lineno = t.value.count('\n')

	# error handling.....?
	def error(self, t):
		print("Illegal character '%s'" % t.value[0])
		self.index += 1
# Lexer Class End

# Parser Class Start
class BasicParser(Parser):
	#tokens are passed from lexer to parser
	tokens = BasicLexer.tokens

	precedence = (
		('left', '+', '-'),
		('left', '*', '/'),
		('right', 'UMINUS'),
		('left', PRINT)
	)

	def __init__(self):
		self.env = { }

	@_('')
	def statement(self, p):
		pass

	@_('var_assign')
	def statement(self, p):
		return p.var_assign

	@_('NAAM "=" expr')
	def var_assign(self, p):
		return ('var_assign', p.NAAM, p.expr)

	@_('NAAM "=" STRING')
	def var_assign(self, p):
		return ('var_assign', p.NAAM, p.STRING)

	@_('expr')
	def statement(self, p):
		return (p.expr)

	@_('STRING')
	def statement(self, p):
		return (p.STRING)

	@_('expr "+" expr')
	def expr(self, p):
		return ('add', p.expr0, p.expr1)

	@_('expr "-" expr')
	def expr(self, p):
		return ('sub', p.expr0, p.expr1)

	@_('expr "*" expr')
	def expr(self, p):
		return ('mul', p.expr0, p.expr1)

	@_('expr "/" expr')
	def expr(self, p):
		return ('div', p.expr0, p.expr1)

	@_('"-" expr %prec UMINUS')
	def expr(self, p):
		print(dir(p))
		return p.expr

	@_('NAAM')
	def expr(self, p):
		return ('var', p.NAAM)

	@_('NUMBER')
	def expr(self, p):
		return ('num', p.NUMBER)

	@_('PRINT statement')
	def statement(self, p):
		return ('print', p.statement)
# Parser Class End

# Execution Class Start
class BasicExecute:
	
	def __init__(self, tree, env):
		self.env = env
		result = self.walkTree(tree)
		if isinstance(result, int) :
			print(result)
		elif isinstance(result, str):
			print(result[1:-1])

	def walkTree(self, node):

		if isinstance(node, int) or isinstance(node, str):
			return node

		if node is None:
			return None

		if node[0] == 'program':
			if node[1] == None:
				self.walkTree(node[2])
			else:
				self.walkTree(node[1])
				self.walkTree(node[2])

		if node[0] == 'num':
			return node[1]

		if node[0] == 'str':
			return node[1]

		if node[0] == 'add':
			return self.walkTree(node[1]) + self.walkTree(node[2])
		elif node[0] == 'sub':
			return self.walkTree(node[1]) - self.walkTree(node[2])
		elif node[0] == 'mul':
			return self.walkTree(node[1]) * self.walkTree(node[2])
		elif node[0] == 'div':
			return self.walkTree(node[1]) / self.walkTree(node[2])
		elif node[0] == 'print':
			return self.walkTree(node[1])

		if node[0] == 'var_assign':
			self.env[node[1]] = self.walkTree(node[2])
			return node[1]

		if node[0] == 'var':
			try:
				return self.env[node[1]]
			except LookupError:
				print("Undefined variable '"+node[1]+"' found!")
				return 0
# Execution Class End

# Execution Start

VERSION = "v0.1 Lawda"

if __name__ == '__main__':
	lexer = BasicLexer()
	parser = BasicParser()
	env = {}

	while True:
		
		try:
			text = input(f'WiseLang: {VERSION}> ')
		
		except (EOFError, KeyboardInterrupt):
			break
		
		if text:
			tree = parser.parse(lexer.tokenize(text))
			BasicExecute(tree, env)
# Execution End
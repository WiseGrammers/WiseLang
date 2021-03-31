# Imports
from sly import Lexer
from sly import Parser
import ast

# Lexer Class Start
class BasicLexer(Lexer):
	tokens = { NAAM, NUMBER, STRING, PRINT, INPUT, WTF, } # PASS, IF, ELIF, ELSE, BREAK, LBRAC, RBRAC, }
	ignore = '\t '
	literals = { '+', '-', '/', '*', '%', 
				'==', '!=', '='}

	# Define tokens as regular expressions
	# (stored as raw strings)
	NAAM = r'[a-zA-Z_][a-zA-Z0-9_]*'
	STRING = r'\".*?\"'
	NAAM["eww"] = PRINT
	NAAM["input"] = INPUT
	# NAAM["chutiya"] = PASS
	# NAAM["agar"] = IF
	# NAAM["agar yeh"] = ELIF
	# NAAM["nahi toh"] = ELSE
	# NAAM["hatt"] = BREAK
	NAAM["WTF"] = WTF

	# Operators
	# LBRAC = r'\{'
	# RBRAC = r'\}'

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
	tokens = BasicLexer.tokens

	precedence = (
		('left', '+', '-'),
		('left', '*', '/'),
		('left', '%'),
		('right', 'UMINUS'),
		('left', PRINT, INPUT)
	)

	def __init__(self):
		self.env = { }

	@_('')
	def statement(self, p):
		pass

	@_('var_assign')
	def statement(self, p):
		return p.var_assign

	@_('WTF NAAM "=" statement')
	def var_assign(self, p):
		return ('var_assign', p.NAAM, p.statement)

	@_('expr')
	def statement(self, p):
		return (p.expr)

	@_('STRING')
	def statement(self, p):
		return ('str', f'"{p.STRING}"')

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

	@_('expr "%" expr')
	def expr(self, p):
		return ('mod', p.expr0, p.expr1)

	@_('"-" expr %prec UMINUS')
	def expr(self, p):
		return ('negate', p.expr)

	@_('NAAM')
	def expr(self, p):
		return ('var', p.NAAM)

	@_('NUMBER')
	def expr(self, p):
		return ('num', p.NUMBER)

	@_('PRINT statement')
	def statement(self, p):
		return ('print', p.statement)

	@_('INPUT statement')
	def statement(self, p):
		return ('input', p.statement)

	# @_('PASS')
	# def statement(self, p):
	# 	pass

	# @_('BREAK')
	# def statement(self, p):
	# 	return ('break', p.BREAK)

	# @_('IF expr LBRAC statement RBRAC [ ELIF expr LBRAC statement RBRAC ] [ ELSE LBRAC statement RBRAC ] ')
	# def statement(self, p):
	# 	return ('if-elif-else', p.expr0 ,p.statements0, p.expr1, p.statements1, p.statements2)

# Parser Class End

# Execution Class Start
class BasicExecute:

	def __init__(self, env, config):
		self.env = env
		self.conf = config

	def run(self, tree):
		result = self.walkTree(tree)
		if result is not None and ((isinstance(result, float), isinstance(result, int)) or isinstance(result, str)):
			return repr(result)

	def walkTree(self, node):

		if self.conf["DEBUG"] == True:
			print("[DEBUG]:", repr(node))

		if node is None:
			return None

		elif node[0] == 'program':
			if node[1] == None:
				self.walkTree(node[2])
			else:
				self.walkTree(node[1])
				self.walkTree(node[2])

		elif node[0] == 'num':
			return node[1]

		elif node[0] == 'str':
			return node[1][1:-1]

		elif node[0] == 'add':
			return self.walkTree(node[1]) + self.walkTree(node[2])

		elif node[0] == 'sub':
			return self.walkTree(node[1]) - self.walkTree(node[2])

		elif node[0] == 'mul':
			return self.walkTree(node[1]) * self.walkTree(node[2])

		elif node[0] == 'div':
			return self.walkTree(node[1]) / self.walkTree(node[2])

		elif node[0] == 'mod':
			return self.walkTree(node[1]) % self.walkTree(node[2])

		elif node[0] == 'negate':
			return -1 * self.walkTree(node[1])

		elif node[0] == 'print':
			tmp = self.walkTree(node[1])
			if tmp is not None:
				print(tmp)
			else:
				print('')
			del tmp

		elif node[0] == 'input':
			optstr = self.walkTree(node[1])
			if optstr is not None:
				return input(optstr)
			return input()

		elif node[0] == 'var_assign':
			self.env[node[1]] = self.walkTree(node[2])

		elif node[0] == 'var':
			try:
				return self.env[node[1]]
			except LookupError:
				print("Undefined variable '"+node[1]+"' found!")

		# elif node[0] == 'break':
			# raise SystemExit


'''don't uncomment this'''
		# elif node[0] == 'if-elif-else':
		# 	expr1 = node[1]
		# 	expr2 = None if node[3] is None else node[3]
		# 	if expr1:
		# 		return node[2]
		# 	elif expr2:
		# 		return node[4]
		# 	else:
		# 		if node[5]:
		# 			return node[5]
		# 		else:
		# 			pass
# Execution Class End

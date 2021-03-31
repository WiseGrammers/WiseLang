from classes import BasicLexer, BasicParser, BasicExecute
import sys

# Default config
config = {
	"DEBUG": False
}

if "-d" in sys.argv:
	config["DEBUG"] = True

# Execution Start
VERSION = "v0.1 Lawda"

if __name__ == '__main__':
	lexer = BasicLexer()
	parser = BasicParser()
	print(f'WiseLang {VERSION}:')
	env = {}
	
	while True:
		
		try:
			text = input('WiseLang > ')
		
		except (EOFError, KeyboardInterrupt):
			break
		
		if text:
			tree = parser.parse(lexer.tokenize(text))
			BasicExecute(tree, env, config)
# Execution End
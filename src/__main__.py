from classes import BasicLexer, BasicParser, BasicExecute
import sys

# Default config
config = {
	"DEBUG": False
}

if "-d" in sys.argv or "--debug" in sys.argv:
	config["DEBUG"] = True

elif "-h" in sys.argv or "--help" in sys.argv:
	__name__ = None
	print("Usage: python3 src/ [options] \n-d, --debug\n\toutputs lex, parse and node details to files.\n-h, --help\n\tDisplayes this Text")

# Execution Start
VERSION = "v0.3 Lawda"

if __name__ == '__main__':
	lexer = BasicLexer()
	parser = BasicParser()
	executor = BasicExecute({}, config)
	print(f'WiseLang {VERSION}:')

	while True:

		try:
			text = input('>>> ')

		except (EOFError, KeyboardInterrupt):
			break

		if text:
			tree = parser.parse(lexer.tokenize(text))
			print(executor.run(tree))
# Execution End
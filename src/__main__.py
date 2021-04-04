from classes import WiseLexer, WiseParser, Executor
import sys, os

# Default config
config = {
	"DEBUG": False,
	"INTERACTIVE": False
}

VERSION = "v0.1.0 Lawda"

# Execution
if __name__ == '__main__':
	if len(sys.argv) > 0 and os.path.isfile(sys.argv[-1]):
		with open(sys.argv[-1]) as f:
			text = f.read()
	else:
		text = None
		config["INTERACTIVE"] = True

	if "-d" in sys.argv or "--debug" in sys.argv:
		config["DEBUG"] = True

	elif "-h" in sys.argv or "--help" in sys.argv:
		print("Usage: python3 src/ [file] [options] \n-d, --debug\n\toutputs lex, parse and node details to files.\n-h, --help\n\tDisplayes this Text")
		sys.exit()

	lexer = WiseLexer()
	parser = WiseParser()
	executor = Executor({}, config)
	print(f'WiseLang {VERSION}:')

	while True:

		try:
			if not text:
				text = input('>>> ')

		except (EOFError, KeyboardInterrupt):
			break

		if text and text != "exit":
			tree = parser.parse(lexer.tokenize(text))
			if tree:
				executor.run(tree)
			if not config["INTERACTIVE"] and not config["DEBUG"]:
				break
			text = None
<<<<<<< HEAD

		elif text and text == "exit":
			print("goodbye.......")
			break
=======
>>>>>>> b8160d59b9b5c0d63406aa3449842bd014b4713a

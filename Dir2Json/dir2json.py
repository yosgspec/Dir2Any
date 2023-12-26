from typing import Final, List
import os
import argparse 
import glob
import json

class Dir2Any:
	def __init__(self, path: str, prompt: str, format: str):
		cd = os.path.dirname(path)
		if cd != "": os.chdir(cd)
		self._prompt: Final[str] = prompt + " $ "
		self._targetDir: Final[str] = os.path.basename(path)
		self._outputFile: Final[str] = f"{self._targetDir}.{format}"
		self.value = ""

	def compress(self):
		print("Compressed!")

	def extract(self):
		print("Extracted!")

	def read(self):
		with open(self._outputFile, 'r') as f:
			self.value = f.read()

	def write(self):
		with open(self._outputFile, "w") as f:
			f.write(self.value)

	def stdin(self):
		self.value = input(self._prompt).strip()

	def stdout(self):
		print(self._prompt)
		print(self.value)


class Dir2Json(Dir2Any):
	__encodings: Final[List[str]]  = [
		"utf_8",
		"cp932",
		"euc_jp"
	]

	def __init__(self, path: str):
		super().__init__(path, "json", "json")
		self.__files = []

	def __getTextAndEncoding(self, file: str):
		for e in Dir2Json.__encodings:
			try:
				with open(file, encoding=e) as f:
					return [f.read(), e]
			except:
				continue
		else:
			with open(file) as f:
				f.read()

	def __readFiles(self):
		os.chdir(self._targetDir)
		self.__files = [
			[f.replace("\\", "/")] + self.__getTextAndEncoding(f)
			for f in glob.glob("./**", recursive=True)
			if not os.path.isdir(f)
		]
		os.chdir("..")

	def __convJson(self):
		self.value = json.dumps(self.__files,separators=(",",":"))

	def __readJson(self):
		self.__files = json.loads(self.value)

	def __makeFiles(self):
		os.makedirs(self._targetDir, exist_ok=True)
		os.chdir(self._targetDir)
		for file, text, e in self.__files:
			os.makedirs("./" + os.path.dirname(file), exist_ok=True)
			with open(file, "w", encoding=e) as f:
				f.write(text)
		os.chdir("..")

	def compress(self):
		self.__readFiles()
		self.__convJson()
		super().compress()

	def extract(self):
		self.__readJson()
		self.__makeFiles()
		super().extract()

def main():
	parser = argparse.ArgumentParser(
		description="Compress targetDir to Json")
	parser.add_argument("targetDir",
		help="target directory")
	parser.add_argument("-e", "--extract",
		action="store_true",
		help="extract from Json to targetDir")
	parser.add_argument("-o", "--outputFile",
		action="store_true",
		help="set input/output to {targetDit}.json")
	args = parser.parse_args()

	d2 = Dir2Json(args.targetDir)
	if not args.extract:
		d2.compress()
		d2.write() if args.outputFile else d2.stdout()
	else:
		d2.read() if args.outputFile else d2.stdin()
		d2.extract()

if __name__ == "__main__":
	main()

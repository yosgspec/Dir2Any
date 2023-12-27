from typing import Final
import os
import argparse 
import shutil
import base64
import uuid

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
		with open(self._outputFile, "r") as f:
			self.value = f.read()

	def write(self):
		with open(self._outputFile, "w") as f:
			f.write(self.value)

	def stdin(self):
		self.value = input(self._prompt).strip()

	def stdout(self):
		print(self._prompt)
		print(self.value)

class Dir2Base64(Dir2Any):
	def __init__(self, path: str):
		super().__init__(path, "base64", "b64")
		self.__tmp = str(uuid.uuid1())
		self.__tmpZip = self.__tmp + ".zip"

	def __makeZip(self):
		shutil.make_archive(self.__tmp, "zip", self._targetDir)

	def __encBase64(self):
		with open(self.__tmpZip, "br") as f:
			self.value = base64.b64encode(f.read()).decode()
		os.remove(self.__tmpZip)

	def __unZip(self):
		shutil.unpack_archive(self.__tmpZip, self._targetDir)
		os.remove(self.__tmpZip)

	def __decBase64(self):
		with open(self.__tmpZip, "bw") as f:
			f.write(base64.b64decode(self.value.encode()))

	def compress(self):
		self.__makeZip()
		self.__encBase64()
		super().compress()

	def extract(self):
		self.__decBase64()
		self.__unZip()
		super().extract()

def main():
	parser = argparse.ArgumentParser(
		description="Compress targetDir to Zip/Base64")
	parser.add_argument("targetDir",
		help="target directory")
	parser.add_argument("-e", "--extract",
		action="store_true",
		help="extract from Zip/Base64 to targetDir")
	parser.add_argument("-o", "--outputFile",
		action="store_true",
		help="set input/output to {targetDit}.b64")
	args = parser.parse_args()

	d2 = Dir2Base64(args.targetDir)
	if not args.extract:
		d2.compress()
		d2.write() if args.outputFile else d2.stdout()
	else:
		d2.read() if args.outputFile else d2.stdin()
		d2.extract()

if __name__ == "__main__":
	main()

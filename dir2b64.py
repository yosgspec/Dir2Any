import sys
import os
import shutil
import base64
import uuid
import argparse 

class Dir2Base64:
	def __init__(self, path: str):
		cd = os.path.dirname(path)
		if cd != "": os.chdir(cd)
		self.targetDir = os.path.basename(path)
		self.targetB64 = f"{self.targetDir}.b64"
		self.tmp = str(uuid.uuid1())
		self.tmpZip = f"{self.tmp}.zip"
		self.prompt = "base64 $ "
		self.value = ""

	def zip(self):
		shutil.make_archive(self.tmp, "zip", self.targetDir)

	def unZip(self):
		shutil.unpack_archive(self.tmpZip, self.targetDir)
		os.remove(self.tmpZip)

	def base64(self):
		with open(self.tmpZip, "br") as f:
			self.value = base64.b64encode(f.read())
		os.remove(self.tmpZip)

	def unBase64(self):
		with open(self.tmpZip, "bw") as f:
			f.write(base64.b64decode(self.value.encode()))

	def read(self):
		with open(self.targetB64, 'r') as f:
			self.value = f.read()

	def write(self):
		with open(self.targetB64,"w") as f:
			f.write(self.value.decode())

	def stdin(self):
		self.value = input(self.prompt).strip()

	def stdout(self):
		print(self.prompt)
		print(str(self.value, "utf-8"))

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

	d2b = Dir2Base64(args.targetDir)

	if args.extract:
		if args.outputFile:
			d2b.read()
		else:
			d2b.stdin()

		d2b.unBase64()
		d2b.unZip()
		print("Extracted!")

	else:
		d2b.zip()
		d2b.base64()

		if args.outputFile:
			d2b.write()
			print("Compressed!")
		else:
			d2b.stdout()

if __name__ == "__main__":
	main()

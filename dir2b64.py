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
		shutil.make_archive(
			self.tmp,
			"zip",
			self.targetDir
		)
		return self

	def unZip(self):
		shutil.unpack_archive(
			self.tmpZip,
			self.targetDir
		)
		return self

	def base64(self):
		with open(self.tmpZip, "br") as f:
			self.value = base64.b64encode(f.read())
		return self

	def unBase64(self):
		with open(self.tmpZip, "bw") as f:
			f.write(base64.b64decode(self.value.encode()))
		return self

	def read(self):
		with open(self.targetB64, 'r') as f:
			self.value = f.read()
		return self

	def write(self):
		with open(self.targetB64,"w") as f:
			f.write(self.value.decode())
		return self

	def stdin(self):
		self.value = input(self.prompt).strip()
		return self

	def stdout(self):
		print(self.prompt)
		print(str(self.value, "utf-8"))
		return self

	def rmZip(self):
		try:
			os.remove(self.tmpZip)
		finally:
			return self

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
	try:
		if args.extract:
			if args.outputFile:
				d2b.read(),
			else:
				d2b.stdin()
			d2b.unBase64().unZip()
			print("Extracted!")

		else:
			d2b.zip().base64()
			if args.outputFile:
				d2b.write()
				print("Compressed!")
			else:
				d2b.stdout()

	finally:
		d2b.rmZip()

if __name__ == "__main__":
	main()

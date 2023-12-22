import sys
import os
import shutil
import base64
import uuid

class Dir2Base64:
	def __init__(self, path):
		cd = os.path.dirname(path)
		os.chdir(cd)
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

	def write(self):
		with open(self.targetB64,"w") as f:
			f.write(self.value.decode())
		return self

	def read(self):
		with open(self.targetB64, 'r') as f:
			self.value = f.read()
		return self

	def stdout(self):
		print(self.prompt)
		print(str(self.value, "utf-8"))
		return self

	def stdin(self):
		self.value = input(self.prompt).strip()
		return self

	def rmZip(self):
		os.remove(self.tmpZip)
		return self

def main():
	"""$ dir2base64 option targetDir

  option:
    -d: targetDir to base64 > stdout
    -fd: targetDir to base64 > base64.textFile
    -b: stdin > base64 to targetDir
    -fb: textFile > base64 to targetDir
"""

	try:
		mode = sys.argv[1]
		path = sys.argv[2]

		try:
			d2b = Dir2Base64(path)
			{
				"-d": lambda: d2b.stdin().unBase64().unZip(),
				"-fd": lambda: d2b.read().unBase64().unZip(),
				"-b": lambda: d2b.zip().base64().stdout(),
				"-fb": lambda: d2b.zip().base64().write()
			}[mode]()

		finally:
			d2b.rmZip()

	except Exception as ex:
		print(main.__doc__)

if __name__ == "__main__":
	main()

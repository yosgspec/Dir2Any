# Dir2Base64
Directory To Zip/Base64 Converter for Python 3

## Usage
```cmd: Windows
C:/> ./dir2base64 samples
```

```sh: *nix
# init
chmod 755 ./dir2base64.sh
./dir2base64.sh samples
```

### Help
```sh
usage: dir2b64.py [-h] [-e] [-o] targetDir

Compress targetDir to Zip/Base64

positional arguments:
  targetDir         Target directory

options:
  -h, --help        show this help message and exit
  -e, --extract     Extract from Zip/Base64 to targetDir
  -o, --outputFile  Set input/output to {targetDit}.b64
```

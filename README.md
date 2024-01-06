# Dir2Any
Directory To Zip/Base64 And Json Converter for Python 3

## Usage
```cmd: Windows
C:/> ./dir2 b64 samples
```

```sh: *nix
# init
chmod 755 ./dir2.sh
./dir2.sh b64 samples
```

### Help
```sh
usage: dir2.py [-h] [-e] [-o] {b64,base64,json} targetDir

Compress targetDir to Zip/Base64 or Json

positional arguments:
  {b64,base64,json}  compress/extract format
  targetDir          target directory

options:
  -h, --help         show this help message and exit
  -e, --extract      extract from Zip/Base64 or Json to targetDir
  -o, --outputFile   set input/output to {targetDit}.b64 or json
```

# barcode-reader

clone project: https://expy-style.net/python/app-bcstockmanager/

## Library setting

```
pip install -r requirements.txt
```

## Run

```
python main.py
```

## Error handlings

### ImportError: Unable to find zbar shared library

Mac の場合下記で解決可能 (https://stackoverflow.com/questions/63217735/import-pyzbar-pyzbar-unable-to-find-zbar-shared-library)

```
brew install zbar

mkdir ~/lib
ln -s $(brew --prefix zbar)/lib/libzbar.dylib ~/lib/libzbar.dylib
```

# wide2long-py

Convert a wide dataset to long format

## Usage

```
usage: wide2long.py [-h] [-d delim] [-o out] [-a [anchor [anchor ...]]]
                    [-D [crop [crop ...]]]
                    FILE

Wide to long

positional arguments:
  FILE

optional arguments:
  -h, --help            show this help message and exit
  -d delim, --delimiter delim
                        Input file delimiter (default: )
  -o out, --outfile out
                        Output filename (default: )
  -a [anchor [anchor ...]], --anchor [anchor [anchor ...]]
                        Anchor fields (default: None)
  -D [crop [crop ...]], --drop [crop [crop ...]]
                        Drop fields (default: None)
```

## Author

Ken Youens-Clark <kyclark@gmail.com>

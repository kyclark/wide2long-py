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

Given an input file like so:

```
$ csvchk tests/addresses.csv
// ****** Record 1 ****** //
first_name   : James
last_name    : Butt
company_name : Benton, John B Jr
address      : 6649 N Blue Gum St
city         : New Orleans
county       : Orleans
state        : LA
zip          : 70116
phone1       : 504-621-8927
phone2       : 504-845-1427
email        : jbutt@gmail.com
web          : http://www.bentonjohnbjr.com
```

The default will be to use the first column as the "anchor" and turn the other columns into a "variable" with the column name and the "value" as the contents of that cell:

```
$ ./wide2long.py tests/addresses.csv
Done, wrote 99 to "tests/addresses_long.csv".
$ csvchk tests/addresses_long.csv -l 3
// ****** Record 1 ****** //
first_name : James
variable   : last_name
value      : Butt
// ****** Record 2 ****** //
first_name : James
variable   : company_name
value      : Benton, John B Jr
// ****** Record 3 ****** //
first_name : James
variable   : address
value      : 6649 N Blue Gum St
```

You can specify more "--anchor" columns:

```
$ ./wide2long.py tests/addresses.csv -a first_name last_name
Done, wrote 90 to "tests/addresses_long.csv".
$ csvchk tests/addresses_long.csv -l 3
// ****** Record 1 ****** //
first_name : James
last_name  : Butt
variable   : company_name
value      : Benton, John B Jr
// ****** Record 2 ****** //
first_name : James
last_name  : Butt
variable   : address
value      : 6649 N Blue Gum St
// ****** Record 3 ****** //
first_name : James
last_name  : Butt
variable   : city
value      : New Orleans
```

If the input file extension is ".csv," then the "-d|--delimiter" is assumed to be ","; otherwise it will default to a tab. 

You can use the "-d|--drop" option to omit any columns from the output file.
For instance, we could drop the "company_name":

```
$ ./wide2long.py tests/addresses.csv --anchor first_name last_name \
  --drop company_name
Done, wrote 81 to "tests/addresses_long.csv".
$ csvchk tests/addresses_long.csv -l 3
// ****** Record 1 ****** //
first_name : James
last_name  : Butt
variable   : address
value      : 6649 N Blue Gum St
// ****** Record 2 ****** //
first_name : James
last_name  : Butt
variable   : city
value      : New Orleans
// ****** Record 3 ****** //
first_name : James
last_name  : Butt
variable   : county
value      : Orleans
```

You can use the "-o|--outfile" option to specify an output filename; otherwise the out file will be the input file name plus "_long".

## Author

Ken Youens-Clark <kyclark@gmail.com>

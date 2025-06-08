# This Is The Change Log For mdpre Markdown Preprocessor

### Releases


### v1.1 - 8 June, 2025

* **ENHANCED** [Issue 35](https://github.com/MartinPacker/mdpre/issues/35): Allow `=colwidth` and `=colalign` multipliers shorthand
* **ENHANCED** [Issue 36](https://github.com/MartinPacker/mdpre/issues/36): Allow `=csv` to specify a dialect
* **ENHANCED** [Issue 37](https://github.com/MartinPacker/mdpre/issues/37): Add `=cellrule` for `=csv` to allow e.g. cell colouring via simple rules
* **ENHANCED** [Issue 39](https://github.com/MartinPacker/mdpre/issues/39): Add `=csvflow` to enable flowing of tables processed with `=csv`
* **FIXED** [Issue 38](https://github.com/MartinPacker/mdpre/issues/38): `=def` line terminated with a space causes a crash


### v1.0 - 25 May, 2025

* **ENHANCED** [Issue 1](https://github.com/MartinPacker/mdpre/issues/1): Filenames on command line
* **DOCUMENTED** [Issue 29](https://github.com/MartinPacker/mdpre/issues/29): Allow variable substitution in commands

### v0.9 - 17 May, 2025

* **ENHANCED** [Issue 33](https://github.com/MartinPacker/mdpre/issues/33): Add environment variables
* **ENHANCED** [Issue 34](https://github.com/MartinPacker/mdpre/issues/34): Support `=ifmatch` & `=ifnonmatch`

### v0.8.1 - 9 May, 2025

* **FIXED** [Issue 32](https://github.com/MartinPacker/mdpre/issues/32): Verbose output for `=def` doesn't cope with colons
* **ENHANCED** [Issue 30](https://github.com/MartinPacker/mdpre/issues/30): Allow Variable To Be Set To stderr Value For a Command
* **ENHANCED** [Issue 31](https://github.com/MartinPacker/mdpre/issues/31): Support `=ifempty` & `=ifnotempty`

### v0.8 - 3 May, 2025

* **ENHANCED** mdpre's `=def` support enhanced for shell commands - if value enclosed in backticks - [Issue 28](https://github.com/MartinPacker/mdpre/issues/28).
* **ENHANCED** Added variables `day`, `month`, `year`.

### v0.7.1 - 21  April, 2025

* **ENHANCED** mdpre's make file fragment supports a variable `makefragment`.

### v0.7 - 20  April, 2025

* **ENHANCED** mdpre writes a make file fragment to file descriptor 3 - if present.

### v0.6.9 - 17  September, 2024

* **FIXED** Used a test for `userid` variable that shouldn't break on Ubuntu - [Issue 26](https://github.com/MartinPacker/mdpre/issues/26)
* **FIXED** Used raw strings for parsing CSV-related control lines - [Issue 27](https://github.com/MartinPacker/mdpre/issues/27)

### v0.6.8 - 8  March, 2024

* **FIXED** The only thing that should be stripped off a line in the main loop is the newline

### v0.6.7 - 17  December, 2023

* **ENHANCED** Any line beginning with `<br/>` is concatenated to the previous line.

### v0.6.6 - 30 November, 2023

* **FIXED** `=cal` was not rendering empty calendar cells properly. Now uses `&nbsp;`.

### v0.6.5 - 17 February, 2023

* **FIXED** Crash with `=ifdef` where the variable **isn't** defined.
* **ENHANCED** Added message if there are too few `=endif`s at the end of the run.

### v0.6.4 - 16 May, 2022

* **FIXED** `=cal` needed 7 cells for all rows.

### v0.6.3 - 5 May, 2022

* **ENHANCED** Added `=rowspan` - to allow easy colouring of text of table rows in a `=csv` / `=endcsv` bracket.

### v0.6.2 - 19 March, 2022

* **ENHANCED** Calendar has month in a heading row.

### v0.6.1 - 17 March, 2022

* **ENHANCED** `=caldays` and `=calnote` support a range of day numbers.

### v0.6 - 16 March, 2022

* **ENHANCED** Month Calendar generation supported -with `=cal` etc.

### v0.5 - 27 November, 2021

* **ENHANCED** Symbol resolution happens inline - which means a symbol can be redefined
* **ENHANCED** Added `=inc` and `=dec` - to increment and decrement values of **integer** variables

### v0.4.7 - 21 November, 2021

* **ENHANCED** Recursion check for `=include`
* **ENHANCED** `=include` resolves symbols in filename

### v0.4.6 - 19 October, 2020

* **ENHANCED** With -v heading levels can go arbitrarily deep

### v0.4.5 - 14 October, 2020

* **FIXED** Did not run with Python 3. Now it does

### v0.4.4 - 7 January, 2020

### v0.4.3 - 10 March, 2019

* **NEW** Added some pre-defined variables

### v0.4.2 - 20 January, 2019

* **NEW** `-d` to define variables
* **NEW** `-c` to wrap everything with `=csv` and `=endcsv`

### v0.4.1 - 12 January, 2019

* **FIXED** `=include` needed rewriting to use a stack.

### v0.4 - 21 October, 2018

* **NEW** `=stop` stops reading in further text

### v0.3 - 1 April, 2018

* **FIXED** makeLink() didn't coalesce multiple minus signs into a single one.
* **FIXED** makeLink() didn't remove double or single quotes.

### v0.2 - 26 March, 2018

* **NEW** [TextBundle](http://textbundle.org) support - both TextPack and TextBundle subformats.

### v0.1 - 17 March, 2018

* **NEW** Backslash (`\`) at end of line joins the next line.

* **NEW** You can specify an automatically-generated Table Of Contents.

* **NEW** Startup banner and normal termination message.

* **NEW** `-h` Help parameter.

* **NEW** `-v` "Verbose Mode" parameter - which just documents files being embedded.

### v0.0 - 12 March, 2018

* **NEW** Initial release


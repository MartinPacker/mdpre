# This Is The Change Log For mdpre Markdown Preprocessor

### Releases


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


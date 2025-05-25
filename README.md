# mdpre Markdown Preprocessor

This Python 3 script allows you to take a file with certain embellishments to Markdown and convert it into regular Markdown

Features include

* Being able to include other files, recursively.
* Being able to conditionally include material.
* Being able to embed a CSV set of data and have it turn into tables, complete with alignment and width options.
* Being able to define and use symbols in your text.

Basic usage:

`mdpre < document.mdp > document.markdown`

It's suggested you use a file extension other than .markdown or .md for the input file. .mdp is the one the developer uses.

mdpre uses stdin and stdout so you can use this as part of a pipeline.
It also uses stderr for all messages.
Verbose mode (`-v`) gives you lots of messages.
You can also specify all files - inout, output, log, makefile fragment - on the command line.

For syntax help use `-h`.

Latest release  is [here](https://github.com/MartinPacker/mdpre).


### Future Python Release Support

Please note, and plan accordingly:

* From 1 April, 2025 releases only supported 3.10 or later
* From 1 April, 2026 expect releases to only support 3.11 or later

md2pre moves forward on Python every so often to:

* Take advantage of new language capabilities
* Remain on a supported Python release with adequate fix likelihood.


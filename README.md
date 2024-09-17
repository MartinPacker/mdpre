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
For syntax help use `-h`.

Latest release (v0.6.9) is [here](https://github.com/MartinPacker/mdpre).

#!/usr/bin/env python3
"""
mdpre.py - Preprocesses a file into Markdown

First argument is file to write to

Reads from stdin

"""

import os
import sys
import csv
import shutil
import zipfile
#import StringIO
import re
import datetime

mdpre_level = "0.4.5"
mdpre_date = "14 October, 2020"


def writeMarkdown(toFile, text):
    toFile.write(text + "\n")


def formatCSV(CSV_lines, colalign, colwidth):
    CSV_reader = csv.reader(CSV_lines)

    # Find out how many columns and prime CSV_lines
    columns = 0
    CSV_lines = []
    for row in CSV_reader:
        columns = max(columns, len(row))
        CSV_lines.append(row)

    # Extend colalign to cover all columns - now we know how many there are
    colalign_len = len(colalign)
    for i in range(colalign_len, columns + 1):
        colalign.append("l")

    # Extend colwidth to cover all columns - now we know how many there are
    colwidth_len = len(colwidth)
    for i in range(colwidth_len, columns + 1):
        colwidth.append(1)

    # Now print the table
    first_row = True
    for row in CSV_lines:
        row_text = "|"
        for col in row:
            row_text = row_text + col + "|"
        writeMarkdown(toFile, row_text)

        titleUnderline = "|"
        if first_row is True:
            for i in range(columns):
                dashes = "-" * colwidth[i]
                if colalign[i] == "r":
                    titleUnderline = titleUnderline + dashes + ":|"
                elif colalign[i] == "c":
                    titleUnderline = titleUnderline + ":" + dashes + ":|"
                elif colalign[i] == "l":
                    titleUnderline = titleUnderline + ":" + dashes + "|"
                else:
                    titleUnderline = titleUnderline + dashes + "|"

            writeMarkdown(toFile, titleUnderline)
            first_row = False
    return


def parse_colalign(colString):
    return colString.rstrip().lstrip().split()


def parse_colwidth(colString):
    colwidths = colString.rstrip().lstrip().split()
    colwidthInt = []
    for c in colwidths:
        colwidthInt.append(int(c))
    return colwidthInt


def parse_def(defString):
    spacePos = defString.find(" ")
    varName = defString[:spacePos]
    residue = defString[spacePos + 1 :]
    if spacePos == -1:
        varType = "F"
        varValue = ""
        varName = defString
    else:
        varType = "T"
        varValue = residue

    return [varName, varType, varValue]


# =ifdef encountered
def handle_ifdef(ifStack, ifdefString, vars):
    verbosity = ""

    for varName, varType, varValue in vars:
        if varName == ifdefString:
            # Variable is defined
            if wantVerbose is True:
                verbosity = "<!--mdpre-ifdef:true:" + varName + "-->"

            ifStack.append(True)

            return [ifStack, verbosity]

    # Variable is undefined
    ifStack.append(False)

    if wantVerbose is True:
        verbosity = "<!--mdpre-ifdef:false:" + ifdefString + "-->"

    return [ifStack, verbosity]


# =ifndef encountered
def handle_ifndef(ifStack, ifndefString, vars):
    verbosity = ""

    for varName, varType, varValue in vars:
        if varName == ifndefString:
            # Variable is defined
            if wantVerbose is True:
                verbosity = "<!--mdpre-ifndef:false:" + ifndefString + "-->"

            ifStack.append(False)

            return [ifStack, verbosity]

    # Variable is undefined
    ifStack.append(True)
    if wantVerbose is True:
        verbosity = "<!--mdpre-ifndef:true:" + ifndefString + "-->"

    return [ifStack, verbosity]


# =endif encountered
def handle_endif(ifStack):
    if wantVerbose is True:
        verbosity = "<!--mdpre-endif:-->"
    else:
        verbosity = ""

    ifStack.pop()

    return [ifStack, verbosity]


def handle_undef(name, vars):
    for var in vars:
        if var[0] == name:
            vars.remove(var)
            return [vars, "<!--mdpre-undef:found:" + name + "-->"]

    return [vars, "<!--mdpre-undef:notfound:" + name + "-->"]


def parse_include(input_file, vars, ifStack, embedLevel):
    input_file2 = []
    for line in input_file:
        if line.startswith("=stop") is True:
            return [True, input_file2, vars]

        if ifStack[-1] is True:
            if line.startswith("=include "):
                include_name = line[9:].rstrip().lstrip()
                if wantVerbose is True:
                    input_file2.append(
                        "<!--mdpre-embed-start:"
                        + str(embedLevel + 1)
                        + ":"
                        + include_name
                        + "-->"
                    )
                with open(include_name, "r") as f:
                    stopIt, include_lines, vars = parse_include(
                        f.readlines(), vars, ifStack, embedLevel + 1
                    )
                for line2 in include_lines:
                    input_file2.append(line2)
                if wantVerbose is True:
                    input_file2.append(
                        "<!--mdpre-embed-stop:"
                        + str(embedLevel + 1)
                        + ":"
                        + include_name
                        + "-->"
                    )
                if stopIt is True:
                    return [stopIt, input_file2, vars]
            elif line.startswith("=def ") is True:
                var = parse_def(line[5:-1].lstrip())
                vars.append(var)
                if wantVerbose is True:
                    varName, varType, varValue = var
                    input_file2.append(
                        "<!--mdpre-def:"
                        + varName
                        + ":"
                        + varType
                        + ":"
                        + varValue
                        + "-->"
                    )
            elif line.startswith("=undef") is True:
                varName = line[7:-1].lstrip()
                vars, verbosity = handle_undef(varName, vars)
                if wantVerbose is True:
                    input_file2.append(verbosity)
            elif line.startswith("=ifdef ") is True:
                ifStack, verbosity = handle_ifdef(
                    ifStack, line[7:].lstrip().rstrip(), vars
                )
                if wantVerbose is True:
                    input_file2.append(verbosity)
            elif line.startswith("=ifndef ") is True:
                ifStack, verbosity = handle_ifndef(
                    ifStack, line[8:].lstrip().rstrip(), vars
                )
                if wantVerbose is True:
                    input_file2.append(verbosity)
            elif line.startswith("=endif") is False:
                input_file2.append(line)
        if line.startswith("=endif") is True:
            ifStack, verbosity = handle_endif(ifStack)
            if wantVerbose is True:
                input_file2.append(verbosity)

    return [False, input_file2, vars]


def replace_varname(varName, variables):
    for var in variables:
        if (var[0] == varName) & (var[1] == "T"):
            # A match so return the value
            return var[2]
    return "&" + varName + ";"


def substitute_variables(input_file, variables):
    input_file2 = []
    for line in input_file:
        fragments = line.split("&")
        ampersands = len(fragments) - 1

        # Output line starts with fragment before the first ampersand
        output_line = fragments[0]

        # Go through the remaining fragments, extracting their data
        for f in range(ampersands):
            fragment = fragments[f + 1]
            semicolonPos = fragment.find(";")
            if semicolonPos == -1:
                # No terminating semicolon
                output_line += "&" + fragment
            else:
                # Terminating semicolon so extract variable name
                varName = fragment[:semicolonPos]
                tail = fragment[semicolonPos + 1 :]
                output_line += replace_varname(varName, variables) + tail

        input_file2.append(output_line)
    return input_file2


def handle_linejoins(input_file):
    input_file2 = []
    output_line = ""
    pending = False
    for line in input_file:
        output_line += line
        if line.endswith("\\\n"):
            # Next line should be concatenated to this one
            output_line = output_line[:-2]
            pending = True
        else:
            # Next line shouldn't be concatenated to this one
            input_file2.append(output_line)
            output_line = ""
            pending = False
    if pending is True:
        input_file2.append(output_line)

    return input_file2


# Returns one item per potential TOC entry. First is level, Second is Text
def extractTableOfContents(input_file):
    toc = []
    minTocLevel = 999
    maxTocLevel = 0
    for line in input_file:
        if line.startswith("######"):
            toc.append((6, line[6:].lstrip().rstrip()))
            maxTocLevel = max(maxTocLevel, 6)
            minTocLevel = min(minTocLevel, 6)
        if line.startswith("#####"):
            toc.append((5, line[5:].lstrip().rstrip()))
            maxTocLevel = max(maxTocLevel, 5)
            minTocLevel = min(minTocLevel, 5)
        if line.startswith("####"):
            toc.append((4, line[4:].lstrip().rstrip()))
            maxTocLevel = max(maxTocLevel, 4)
            minTocLevel = min(minTocLevel, 4)
        elif line.startswith("###"):
            toc.append((3, line[3:].lstrip().rstrip()))
            maxTocLevel = max(maxTocLevel, 3)
            minTocLevel = min(minTocLevel, 3)
        elif line.startswith("##"):
            toc.append((2, line[2:].lstrip().rstrip()))
            maxTocLevel = max(maxTocLevel, 2)
            minTocLevel = min(minTocLevel, 2)
        elif line.startswith("#"):
            toc.append((1, line[1:].lstrip().rstrip()))
            maxTocLevel = max(maxTocLevel, 1)
            minTocLevel = min(minTocLevel, 1)
    return [minTocLevel, maxTocLevel, toc]


def parseTocStatement(line, minTocLevel, maxTocLevel):
    TocParms = line[5:].lstrip().rstrip()
    if TocParms == "":
        # No parms so return defaults - full depth and "Contents"
        return [minTocLevel, maxTocLevel, "Contents"]
    else:
        # Have parms so parse them
        TocParmsArray = TocParms.split(" ")
        if TocParmsArray[0].isdigit() is True:
            # First parm is either max or min level spec
            level1 = int(TocParmsArray[0])
            if len(TocParmsArray) == 1:
                # First parm is only parm so it is the max level
                return [minTocLevel, level1, "Contents"]
            elif TocParmsArray[1].isdigit() is True:
                # Second parm is also a number so have both min and max
                level2 = int(TocParmsArray[1])
                if len(TocParmsArray) == 2:
                    # Have both numeric parms and no title
                    return [level1, level2, "Contents"]
                else:
                    # Have both numeric parms and a title
                    return [level1, level2, TocParms[4:]]
            elif TocParmsArray[1] == "*":
                # Top level limited by levels available
                level2 = maxTocLevel
                if len(TocParmsArray) == 2:
                    # Have both range parms and no title
                    return [level1, level2, "Contents"]
                else:
                    # Have both range parms and a title
                    return [level1, level2, TocParms[4:]]
        elif TocParms != "":
            # Have just the title
            return [minTocLevel, maxTocLevel, TocParms]


def makeLink(linkText):
    linkURL = (
        linkText.replace("-", "")
        .replace(" ", "-")
        .replace("?", "")
        .replace("`", "")
        .replace("=", "")
        .replace(",", "")
        .replace(":", "")
        .replace(".", "")
        .replace("\\", "")
        .replace('"', "")
        .replace("'", "")
        .lower()
        .rstrip("-")
    )
    return re.sub(r"-+", "-", linkURL)


# Print Table Of Contents down to maximum level
def printTableOfContents(minLevel, maxLevel, heading, toc):
    writeMarkdown(toFile, heading + "\n")
    for tocEntryLevel, tocEntryText in toc:
        if (tocEntryLevel >= minLevel) & (tocEntryLevel <= maxLevel):
            writeMarkdown(
                toFile,
                ("\t" * (tocEntryLevel - minLevel))
                + "* ["
                + tocEntryText
                + "](#"
                + makeLink(tocEntryText)
                + ")",
            )


def handle_verbose(line):
    noPrefixSuffix = line[10:-3]
    verboseArray = noPrefixSuffix.split(":")
    verboseType = verboseArray[0]
    if verboseType == "embed-start":
        embedLevel = int(verboseArray[1])
        sys.stderr.write(("---" * embedLevel) + "> Start of " + verboseArray[2] + "\n")
    elif verboseType == "embed-stop":
        embedLevel = int(verboseArray[1])
        sys.stderr.write(("---" * embedLevel) + "> End of " + verboseArray[2] + "\n")
    elif verboseType == "heading":
        sys.stderr.write(line[18:-3].replace("#", "..... ")[6:].lstrip() + "\n")
    elif verboseType == "toc":
        sys.stderr.write("Table Of Contents - spec '" + noPrefixSuffix[9:] + "'\n")
    elif verboseType == "csv":
        sys.stderr.write("CSV Start\n")
    elif verboseType == "endcsv":
        sys.stderr.write("CSV Stop\n")
    elif verboseType == "colalign":
        sys.stderr.write("Column Alignment - spec '" + noPrefixSuffix[19:] + "'\n")
    elif verboseType == "colwidth":
        sys.stderr.write("Column Width - spec '" + noPrefixSuffix[19:] + "'\n")
    elif verboseType == "def":
        if verboseArray[2] == "T":
            sys.stderr.write("Def " + verboseArray[1] + " = " + verboseArray[3] + "\n")
        else:
            sys.stderr.write("Def " + verboseArray[1] + "\n")
    elif verboseType == "undef":
        if verboseArray[1] == "found":
            sys.stderr.write("Undef successful " + verboseArray[2] + "\n")
        else:
            sys.stderr.write("Undef failed " + verboseArray[2] + "\n")
    elif verboseType == "endif":
        sys.stderr.write("Endif\n")
    elif verboseType == "ifdef":
        if verboseArray[1] == "true":
            sys.stderr.write("Ifdef true " + verboseArray[2] + "\n")
        else:
            sys.stderr.write("Ifdef nottrue " + verboseArray[2] + "\n")
    elif verboseType == "ifndef":
        if verboseArray[1] == "true":
            sys.stderr.write("Ifndef true " + verboseArray[2] + "\n")
        else:
            sys.stderr.write("Ifndef untrue " + verboseArray[2] + "\n")
    else:
        sys.stderr.write("Unknown " + line + "\n")

    return


def handle_adjustGraphics(line):
    adjustedLine = ""
    splitStart = line.split("![")
    fragment = 0
    for s in splitStart:
        if fragment == 0:
            # Before first ![
            adjustedLine = s + "!["
        else:
            # At first or subsequent ![
            endLabelPos = s.find("](")
            beginGraphicPos = endLabelPos + 2
            adjustedLine += s[:beginGraphicPos]
            endGraphicPos = s.find(")")

            # Extract original graphic name, including subdirs
            graphic = s[beginGraphicPos:endGraphicPos]

            # Adjust graphic so it's in the assets subfolder
            lastSlash = graphic.rfind("/")
            if lastSlash == -1:
                adjustedGraphic = "assets/" + graphic
            else:
                adjustedGraphic = "assets/" + graphic[lastSlash + 1 :]

            adjustedLine = adjustedLine + adjustedGraphic + ")" + s[endGraphicPos + 1 :]

            # Copy the file into the text bundle
            shutil.copy(graphic, realpath + "/" + adjustedGraphic)
        fragment += 1
    if wantVerbose is True:
        sys.stderr.write("Adjusting >>" + adjustedLine + "<<<\n")

    writeMarkdown(toFile, adjustedLine)

    return


# Handle a -d command line parameter
def handleCommandLineDefine(defString):
    equalsPos = defString.find("=")
    if equalsPos > -1:
        # Assign a value to the variable
        name = defString[:equalsPos]
        value = defString[equalsPos + 1 :]
        parmVars.append("=def " + name + " " + value)
    else:
        # No value to assign so just define it
        name = defString
        parmVars.append("=def " + name)


# Set up standard variables
def setupStandardVariables():
    now = datetime.datetime.now()
    runTime = now.strftime("%H&colon;%M").lstrip()
    runDate = now.strftime("%e %B&comma; %G").lstrip()

    input_file.insert(0, "=def date " + runDate + " ")
    input_file.insert(0, "=def time " + runTime + " ")
    input_file.insert(0, "=def userid " + os.getlogin() + " ")
    input_file.insert(0, "=def mdpre_level " + mdpre_level + " ")
    input_file.insert(0, "=def mdpre_date " + mdpre_date + " ")


BOLD = "\033[1m"
END = "\033[0m"

banner = "mdpre Markdown Preprocessor v" + mdpre_level + " (" + mdpre_date + ")"
bannerUnderline = "=" * len(banner)

sys.stderr.write("\n" + banner + "\n" + bannerUnderline + "\n")

wantVerbose = False

wantTextBundle = False
wantTextPack = False
awaitingFilename = False
textBundleFilename = ""

wrapInCSV = False

parmVars = []

arguments = len(sys.argv) - 1
for arg in range(1, arguments + 1):
    argument = sys.argv[arg]
    if argument == "-h":
        # Print help
        sys.stderr.write(
            "\n\nThe mdpre program is a Markdown preprocessor, making writing complex\nMarkdown documents easier.\n\n"
        )
        sys.stderr.write(
            "\n" + BOLD + "Usage:" + END + "\n\nmdpre < inputfile > outputfile\n\n"
        )
        sys.stderr.write("which processes from inputfile to outputfile.\n\n")

        sys.stderr.write(BOLD + "or:\n\n" + END)
        sys.stderr.write("mdpre -h\n\n")
        sys.stderr.write("which generates this help.\n\n")

        sys.stderr.write(BOLD + "or:\n\n" + END)
        sys.stderr.write("mdpre -v < inputfile > outputfile\n\n")
        sys.stderr.write('which writes additional information in "verbose mode".\n\n')

        sys.stderr.write(BOLD + "or:\n\n" + END)
        sys.stderr.write("mdpre -t < inputfile outputdir\n\n")
        sys.stderr.write(
            "which creates a textbundle directory from inputfile. -v can be used with -t.\n\n"
        )

        sys.stderr.write(BOLD + "or:\n\n" + END)
        sys.stderr.write("mdpre -z < inputfile outputfile\n\n")
        sys.stderr.write(
            "which creates a textpack (zipped textbundle) file from inputfile. -v can be used with -z.\n\n"
        )

        sys.stderr.write("\n\n" + BOLD + "Variables\n\n" + END)
        sys.stderr.write(BOLD + "---------\n\n" + END)
        sys.stderr.write(
            "\nYou can define a variable without a value with the -d flag:\n\n"
        )
        sys.stderr.write("mdpre -dfred < inputfile outputfile\n\n")
        sys.stderr.write(
            "You can define a variable with a value also with the -d flag:\n\n"
        )
        sys.stderr.write("mdpre '-djon=bon jovi' < inputfile outputfile\n\n")
        sys.stderr.write(
            "In this case quotes were used to allow a variable to take a value with spaces in.\n\n"
        )

        sys.stderr.write("\n\n" + BOLD + "Process As A CSV File\n\n" + END)
        sys.stderr.write(BOLD + "---------------------\n\n" + END)
        sys.stderr.write(
            "\nmdpre can treat the whole input file as a CSV file, creating a Markdown table from it, if you specify the -c flag:\n\n"
        )
        sys.stderr.write("mdpre -c < input.csv outputfile\n\n")

        sys.exit()
    elif argument == "-v":
        # Turn on "verbose mode"
        wantVerbose = True
    elif argument == "-t":
        wantTextBundle = True
        wantTextPack = False
        awaitingFilename = True
    elif argument == "-z":
        wantTextBundle = True
        wantTextPack = True
        awaitingFilename = True
    elif argument[:2] == "-d":
        handleCommandLineDefine(argument[2:])
    elif argument == "-c":
        wrapInCSV = True
    elif awaitingFilename is True:
        if textBundleFilename == "":
            textBundleFilename = argument
        else:
            textBundleFilename = textBundleFilename + " " + argument

# Preliminaries if creating a textbundle
if textBundleFilename != "":
    realpath = os.path.realpath(textBundleFilename)
    if wantTextPack is True:
        zippath = realpath
        realpath = realpath + "-temp"

    if wantVerbose is True:
        sys.stderr.write("Writing to Textbundle " + realpath + "\n\n")

    # Check if path exists as a directory
    if os.path.exists(realpath):
        if os.path.isfile(realpath) is True:
            # Regular file of that name exists so quitting
            sys.stderr.write(realpath + " is a regular file. Quitting.\n")
            exit(0)
        else:
            # Directory already exists
            if wantVerbose is True:
                sys.stderr.write(
                    "Directory exists so not creating. It might already have files, some of which might be overwritten.\n\n"
                )
    else:
        # Directory doesn't exist so create it
        if wantVerbose is True:
            sys.stderr.write("Directory does not exist - so creating.\n\n")
        os.mkdir(realpath)

    # Check if assets path exists
    assets = realpath + "/assets"
    if os.path.exists(assets):
        if wantVerbose is True:
            sys.stderr.write("assets directory exists so not creating.\n\n")
    else:
        if wantVerbose is True:
            sys.stderr.write("Creating assets directory.\n\n")
        os.mkdir(assets)

    # Add info.json file
    infoJSON = open(realpath + "/info.json", "w")
    infoJSON.write("{\n")
    infoJSON.write(' "version": 2\n')
    # infoJSON.write(' "type": "net.daringfireball.markdown"\n')

    infoJSON.write("}\n")
    infoJSON.close()

    markdownFile = realpath + "/text.markdown"

    # Remove any prior instance of the markdown file
    if os.path.isfile(markdownFile) is True:
        os.remove(markdownFile)

    # Open the file where markdown goes for write
    toFile = open(markdownFile, "w")
else:
    # Write to stdout as not making a textbundle
    toFile = sys.stdout

input_file = sys.stdin.readlines()

# If -c was specified on the command line wrap the file with =csv / =endcsv bracket
if wrapInCSV == True:
    input_file.insert(0, "=csv")
    input_file.append("=endcsv")

# Add any command line defines to the front
for parmVar in parmVars:
    input_file.insert(0, parmVar + " ")

# insert standard variables at the front
setupStandardVariables()


ifStack = [True]

# Pre-process - to pick up includes
stopIt, input_file, variables = parse_include(input_file, [], ifStack, 0)

# Substitute any variables
input_file = substitute_variables(input_file, variables)

# Handle line joining
input_file = handle_linejoins(input_file)

# Generate Table Of Contents - even if it's not needed
minTocLevel, maxTocLevel, tableOfContents = extractTableOfContents(input_file)

# Do any other processing, such as CSV to table

csv_colalign = []
csv_colwidth = []
in_csv = False

for line in input_file:
    line = line.rstrip()
    if line.startswith("<!--mdpre-"):
        # For verbose mode writing to stderr
        handle_verbose(line)
    elif line.startswith("#"):
        if wantVerbose is True:
            handle_verbose("<!--mdpre-heading:" + line + "-->")
        writeMarkdown(toFile, line)
    elif line.startswith("=toc"):
        if wantVerbose is True:
            handle_verbose("<!--mdpre-toc:" + line + "-->")
        minLevel, maxLevel, heading = parseTocStatement(line, minTocLevel, maxTocLevel)
        printTableOfContents(minLevel, maxLevel, "### " + heading, tableOfContents)
    elif (line.startswith("=csv")) & (in_csv is False):
        in_csv = True
        CSV_lines = []
        if wantVerbose is True:
            handle_verbose("<!--mdpre-csv:" + line + "-->")
    elif (line.startswith("=endcsv")) & (in_csv is True):
        formatCSV(CSV_lines, csv_colalign, csv_colwidth)
        in_csv = False
        if wantVerbose is True:
            handle_verbose("<!--mdpre-endcsv:" + line + "-->")
    elif line.startswith("=colalign "):
        csv_colalign = parse_colalign(line[10:])
        if wantVerbose is True:
            handle_verbose("<!--mdpre-colalign:" + line + "-->")
    elif line.startswith("=colwidth "):
        csv_colwidth = parse_colwidth(line[10:])
        if wantVerbose is True:
            handle_verbose("<!--mdpre-colwidth:" + line + "-->")
    elif in_csv is True:
        CSV_lines.append(line)
    elif (line.find("![") > -1) & (wantTextBundle is True):
        # Fix up graphics references and copy graphics to assets folder
        handle_adjustGraphics(line)
    else:
        writeMarkdown(toFile, line)

toFile.close()

if wantTextPack is True:
    if wantVerbose is True:
        print("Archiving " + realpath + " to " + zippath + ".zip")
    shutil.make_archive(zippath, "zip", realpath)

    if wantVerbose is True:
        print("Renaming " + zippath + ".zip to " + zippath)
    os.rename(zippath + ".zip", zippath)

    if wantVerbose is True:
        print("Removing temporary files in directory " + realpath)
        shutil.rmtree(realpath)
sys.stderr.write("\nProcessing completed.\n\n")


exit()

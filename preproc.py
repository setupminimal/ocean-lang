#! /usr/bin/env python3

# preproc.py

# By Daroc Alden

# Do you dislike the construct
# int main(int stuff, int things) {
#     return stuff;
# }
# and wish it would look like
# int main <- int stuff, int things:
#     return stuff;

indentMarker = ":"

passes = []

def _pass(f):
    global passes
    passes.append(f)
    return f

def iterate(f):
    def inn(src):
        oldSrc = list(src)
        newSrc = list(f(oldSrc))
        while oldSrc != newSrc:
            oldSrc = newSrc
            newSrc = list(f(oldSrc))
        yield from newSrc
    return inn

# Pass Generator
# Accepts [line], transforms "arrow stuff end" into (stuff), yields [line]
def parens(arrow, end, rep1="(", rep2=")"):
    def transform(src):
        for line in src:
            if arrow in line and end in line: # Otherwise we don't want to process these
                if line.count('"') % 2 != 0:
                    print("""There is a line with an odd number of "s.
                    I'm not really sure how to deal with this.
                    I'm going to pretend that everything is fine, but it probably isn't.""")
                    print("Here is the affected line:")
                    print(line)
                    print()
                acc = ""
                while '"' in line: # This will be skipped if there are no "s.
                    pos = line.index('"')
                    acc += line[:pos].replace(arrow, rep1, 1).replace(end, rep2, 1)
                    acc += '"'
                    line = line[pos+1:]
                    pos = line.index('"')
                    acc += line[:pos]
                    acc += '"'
                    line = line[pos+1:]
                acc += line.replace(arrow, rep1, 1).replace(end, rep2, 1)
                yield acc
            else:
                yield line # This is a plain line

    transform = iterate(transform)
    _pass(transform)
    return transform

# Accepts string, yields [line]
@_pass
def breakLines(src):
    yield from src.split("\n")

# Accepts [line], yields [line] with right-hand whitespace removed
@_pass
def rstrip(src):
    for line in src:
        yield line.rstrip()

# Accepts [line], yields [line] with appropriate ;s
@_pass
def placeSemicolons(src):
    def ok(line, inMultilineComment):
        return  (line != "" and 
                 not line.endswith(indentMarker) and
                 not line.endswith(";") and 
                 not "//" in line and
                 not line.strip().startswith("#") and
                 not inMultilineComment and
                 not "*/" in line)
    inMultilineComment = False
    for line in src:
        if "/*" in line and not inMultilineComment:
            # This could still be broken by // /* blah ...
            inMultilineComment = True
        if inMultilineComment and "*/" in line:
            inMultilineComment = False
        if ok(line, inMultilineComment):
            yield line + ";"
        elif "//" in line:
            if line.strip().startswith("//"):
                yield line
            elif ok(line[:line.index("//")], inMultilineComment):
                yield line[:line.index("//")] + "; " + line[line.index("//"):]
        else:
            yield line

# Accepts [line], yields [(indent, line)]
@_pass
def annotateIndent(src, spacePerTab=4):
    for line in src:
        line = line.replace("\t", " "*spacePerTab)
        space = len(line) - len(line.strip())
        yield space, line

# Accepts [(indent, line)], yields [line] with braces in correct place
@_pass
def placeBraces(src):
    prevIndent = 0
    inMultiline = False
    for indent, line in src:
        if "/*" in line:
            inMultiline = True
        if inMultiline:
            if "*/" in line:
                inMultiline = False
            yield line
            continue

        if indent > prevIndent:
            prevIndent = indent
        if indent < prevIndent and line != "":
            yield " "*indent + "}"

        yield line

        if line.endswith(indentMarker):
            yield " "*indent + "{"

# Takes [line], and puts blank lines after "}"s they procede
@_pass
def rearrangeBlank(src):
    stack = []
    for line in src:
        if line == "":
            stack.append(line)
        elif line.strip() == "}":
            yield line
            yield from stack
            stack = []
        else:
            yield from stack
            stack = []
            yield line

# "if condition:" into "if (condition)"
elseIf = parens("if ", indentMarker, "if (", ")")

# "else:" into "else"
elseColon = parens("else", indentMarker, "else", "")

# "<- stuff:" into (stuff)
functionDefinitionArrow = parens(" <-", indentMarker)

# "← stuff:" into (stuff)
functionDefinitionFancyArrow = parens(" ←", indentMarker)

# " $ stuff;" into (stuff);
functionApplicationArrow = parens(" $", ";", rep2=");")

# " $ stuff |" into (stuff)
functionApplicationExplicitBar = parens("$", "|")

# Remove spaces from inside parens
leftParenSpace = parens("( ", "", "(", "")
rightParenSpace = parens(" )", "", ")", "")

# Remove spaces before ;s
semicolonSpace = parens(" ;", "", ";", "")

# Better pointers ?

# Turns [line] into string
def stickTogether(src):
    return "\n".join(src) + "\n\n"

def compile(src):
    for p in passes:
        src = p(src)
    return src

if __name__ == "__main__":
    print("Ocean Compiler v1.0")
    print()
    
    import sys

    with open(sys.argv[1], 'r') as f:
        src = f.read()
        
    with open(sys.argv[1][:-3] + ".c", 'w') as f: # [:-3] removes the ".ca"
        f.write(stickTogether(compile(src)))

    print("Complete.")

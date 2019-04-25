import difflib
from difflib import *

def diff_word():
    '''按照字比较两个文件不同'''

    d = Differ()
    with open('lfile.tmp') as fd:
        lfile = fd.read()

    with open('rfile.tmp') as fd:
        rfile = fd.read()

    # result = list(d.compare(lfiles, rfiles))
    result = list(d.compare(lfile, rfile))

    lfile = []
    rfile = []
    for line in result:
        if line.startswith(' '):
            line = line[2:]
            lfile.append(f'<span class="orig">{line}</span>')
            rfile.append(f'<span class="orig">{line}</span>')
        elif line.startswith('- '):
            line = line[2:]
            lfile.append(f'<span class="red">{line}</span>')
        elif line.startswith('+ '):
            line = line[2:]
            rfile.append(f'<span class="red">{line}</span>')
        elif line.startswith('?'):
            continue
    lfile = ''.join(lfile)
    rfile = ''.join(rfile)

    return {'lfile': lfile, 'rfile': rfile}


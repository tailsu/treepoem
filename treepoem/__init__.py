# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import codecs
import io
import os
import subprocess

from PIL.EpsImagePlugin import EpsImageFile

BASE_DIR = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
BWIPP_PATH = os.path.join(BASE_DIR, 'postscriptbarcode', 'barcode.ps')

BASE_PS = """\
{bwipp}

/Helvetica findfont 10 scalefont setfont
gsave
2 2 scale
10 10 moveto

{code}
/uk.co.terryburton.bwipp findresource exec
grestore

showpage
"""

# Error handling from https://github.com/bwipp/postscriptbarcode/wiki/Developing-a-Frontend-to-BWIPP#use-bwipps-error-reporting
BBOX_TEMPLATE = """\
%!PS

errordict begin
/handleerror {{
  $error begin
  errorname dup length string cvs 0 6 getinterval (bwipp.) eq {{
    (%stderr) (w) file
    dup (\nBWIPP ERROR: ) writestring
    dup errorname dup length string cvs writestring
    dup ( ) writestring
    dup errorinfo dup length string cvs writestring
    dup (\n) writestring
    dup flushfile end quit
  }} if
  end //handleerror exec
}} bind def
end

""" + BASE_PS

EPS_TEMPLATE = """\
%!PS-Adobe-3.0 EPSF-3.0
{bbox}

""" + BASE_PS

BBOX_COMMAND = ['/usr/bin/gs', '-sDEVICE=bbox', '-dBATCH', '-dSAFER', '-']


class PostscriptError(RuntimeError):
    pass


# Inline the BWIPP code rather than using the run operator to execute
# it because the EpsImagePlugin runs Ghostscript with the SAFER flag,
# which disables file operations in the PS code.
def _get_bwipp():
    with open(BWIPP_PATH) as f:
        return f.read()


def _get_bbox(code):
    full_code = BBOX_TEMPLATE.format(bwipp=_get_bwipp(), code=code)
    gs_process = subprocess.Popen(
        BBOX_COMMAND,
        universal_newlines=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    _, err_output = gs_process.communicate(full_code, timeout=2)
    err_output = err_output.strip()
    # Unfortunately the error-handling in the postscript means that
    # returncode is 0 even if there was an error, but this gives
    # better error messages.
    if gs_process.returncode != 0 or 'BWIPP ERROR:' in err_output:
        if err_output.startswith('BWIPP ERROR: '):
            err_output = err_output.replace('BWIPP ERROR: ', '', 1)
        raise PostscriptError(err_output)
    return err_output


def _encode(data):
    return codecs.encode(data.encode('utf8'), 'hex').decode('ascii')


def _format_code(barcode_type, data, options):
    return '<{data}> <{options}> <{barcode_type}> cvn'.format(
        data=_encode(data),
        options=_encode(options),
        barcode_type=_encode(barcode_type),
    )


def generate_barcode(barcode_type, data, options):
    code = _format_code(barcode_type, data, options)
    bbox_lines = _get_bbox(code)
    full_code = EPS_TEMPLATE.format(bbox=bbox_lines, bwipp=_get_bwipp(), code=code)
    return EpsImageFile(io.BytesIO(full_code.encode('utf8')))



# image = generate_barcode('qrcode', "This is ( xtian's barcode yay yay yay yay yay", 'version=10 eclevel=Q something')
# image.save('output.png')

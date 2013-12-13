import sys
from inspect import currentframe, getframeinfo

frameinfo = getframeinfo(currentframe())
error = "ERROR: Cannot divide by Zero File: %s line number: %s"\
         % (getframeinfo(currentframe()).filename , getframeinfo(currentframe()).lineno)

sys.stderr.write(error)
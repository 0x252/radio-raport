import re
def isValidCallSign(callSign): return re.compile(r'^[A-Z]{1,2}[0-9]{1,4}[A-Z]{1,3}$').match(callSign)
# TODO: To an another a file
def debug(*args): # va_list
    if DEBUG_ENABLED:
        print(args)
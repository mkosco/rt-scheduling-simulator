from pprint import pprint
DEBUG = False

def debug_print(message):
    if DEBUG:
        print(message)

def debug_pprint(data):
    if DEBUG:
        pprint(data)
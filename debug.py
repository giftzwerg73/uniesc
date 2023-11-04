dbgen = 0

def dbgprint(txt):
    global dbgen
    if dbgen:
        print(str(txt))
    
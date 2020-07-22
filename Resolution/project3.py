clauses = list()
resolvents = list()
DEBUG = False

def get_input(fname):
    try:
        f = open(fname, "r")
        lines = f.readlines()
        for l in lines: 
            l = l.strip()
            l = l.replace(" ", "")
            split_l = l.split("v")
            clauses.append(split_l)
        f.close()
    except IOError:
        print("File not found. ")

def pl_resolve(clause1, clause2):
    a, b = clause1.copy(), clause2.copy()
    for itemA in clause1: 
        for itemB in clause2:
            if (itemA == ("¬"+itemB)) or (itemB == ("¬"+itemA)): 
                a.remove(itemA)
                b.remove(itemB)
            elif (itemA == itemB):
                a.remove(itemA)
            else:
                continue
    resolvent = a + b
    return resolvent

def pl_resolution():
    global clauses, resolvents
    get_input("input.txt")
    while len(clauses) != 0:
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                resolve = pl_resolve(clauses[i], clauses[j])
                if len(resolve) == 0:
                    return True
                else:
                    resolvents.append(resolve)
                if DEBUG:
                    print("Clauses: %s %s" % (clauses[i], clauses[j]))
                    print("Resolved: %s " % resolve)
        flag = True
        for r in resolvents:
            if r not in clauses:
                flag = False
                break
        if flag:
            return False
        clauses = clauses + resolvents

if __name__ == "__main__":
    print(pl_resolution())
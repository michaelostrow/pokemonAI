import xlrd
import string

poke_sheet = xlrd.open_workbook('pokemon_data.xls').sheet_by_index(0)

sheet_data = range(18)
sheet_data.remove(0)


def make_poke_dict():
    val = {}
    for i in sheet_data:
        val[str(poke_sheet.cell(0, i).value)] = i
    return val

poke_dict = make_poke_dict()

def make_weaks_dict(t):
    val = {}
    for i in sheet_data:
        val[str(poke_sheet.cell(i, 0).value)] = poke_sheet.cell(i, poke_dict[t]).value
    return val

def dual_type_weaks(t1, t2):
    val = make_weaks_dict(t1)
    if t2:
        v2 = make_weaks_dict(t2)
        for x in val:
            val[x] = val[x] * v2[x]
    return val

class Type:
    def __init__(self, t1, t2=None):
        self.t1 = t1
        self.t2 = t2
        self.weaks = dual_type_weaks(t1, t2)
        
    def resist_stabs(self, ty):
        vals = [self.weaks[ty.t1], None]
        if ty.t2:
            vals[1] = self.weaks[ty.t2]
        return vals[0] < 1 and vals[1] < 1

def type_list():
    val = []
    p = poke_dict.keys()
    t1 = 0
    while len(p) > 0:
        if t1 == 0:
            val.append(Type(p[0]))
            t1 = t1 + 1
        elif t1 == len(p):
            t1 = 0
            p.pop(0)
        else:
            val.append(Type(p[0], p[t1]))
            t1 = t1 + 1
    return val

type_list = type_list()

def resisting_types(t):
    l = list(type_list)
    val = []
    for ty in l:
        if ty.resist_stabs(t):
            val.append(ty)
    return val


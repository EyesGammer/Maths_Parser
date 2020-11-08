#!/bin/python3

import math as m

global o_t
o_t = {"+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y, "/": lambda x, y: x / y}

def isn(x):
    try:
        x = int(x)
    except ValueError:
        return (False, x)
    return (True, x)

def diff(a, b, c=[]):
    if a == b:
        return (c, b)
    mi, ma = min(len(a), len(b)), max(len(a), len(b))
    if ma > mi:
        for i, x in enumerate(b):
            if b[i] != a[i]:
                break
    c.append(i)
    return diff(a, b[:i] + a[i] + b[i:], c)

def parser(s, v={}):
    o, n, f, oi, fi, nf = ["+", "-", "*", "/"], [], [], {}, [], []
    def operators(a, b, t=""):
        if b == -1:
            return a
        t = "".join(a) if t == "" else t
        n = [y for x in [x.split(o[b]) for x in t] for y in x]
        oi[o[b]], tmp = diff(t, "".join(n), [])
        return operators(n, b - 1, tmp)
    for x in operators([s], len(o) - 1):
        tmp = isn(x)
        if tmp[0]:
            n.append(tmp[1])
        else:
            f.append(tmp[1])
    def functions(a, b):
        if b == -1:
            return a
        for i, x in enumerate(a[b]):
            if x == "(":
                fi.append(a[b][:i])
                f[b] = getattr(m, a[b][:i])
                break
        return functions(a, b - 1)
    def parse_functions(a):
        b = []
        for y in range(a.count("(")):
            for i, x in enumerate(a):
                if x == "(":
                    b.append(a[:i + 1])
                    a = a[i + 1:]
                    break
        return b
    for x in f:
        for y in parse_functions(x):
            nf.append(y)
    f = nf
    functions(f, len(f) - 1)
    return [s, n, f, v, oi, fi]

def calculator(a):
    s, n, f, v, oi, fi = a
    res = n[0]
    print(s, n, f, v, oi, fi)
    def main(a, b, c, d=""):
        if len(a) == 0:
            return b
        h, tmp = "", a.pop(0)
        for x, i in oi.items():
            for v in i:
                if v == c + 2:
                    h = x
        if d != "":
            b = o_t.get(d)(b, tmp)
        return main(a, b, c + 2, h)
    return main(n, res, -1)

t = parser("2*2", {})
print(calculator(t))

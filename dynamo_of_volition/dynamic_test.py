from dynamic_scope import get_dynamic_re

def outer():
    a = "outer_a"
    b = "outer_b"
    c = "outer_c"
    d = "outer_d"
    e = "outer_e"

    def inner1():
        a = "inner1_a"
        b = "inner1_b"
        inner3("parameter_d")

    def inner2():
        a = "inner2_a"
        b = "inner2_b"
        inner3("parameter_d")

    def inner3(d):
        e = "inner3_e"
        print(f"statically scoped value of a: {a}")
        print(f"statically scoped value of b: {b}")
        print(f"statically scoped value of c: {c}")
        print(f"statically scoped value of d: {d}")
        print(f"statically scoped value of e: {e}")
        dre = get_dynamic_re()
        print(f"dynamically scoped value of a: {dre['a']}")
        print(f"dynamically scoped value of b: {dre['b']}")
        print(f"dynamically scoped value of c: {dre['c']}")
        print(f"dynamically scoped value of d: {dre['d']}")
        print(f"dynamically scoped value of e: {dre['e']}")

    print("Calling inner1:")
    inner1()

    print("Calling inner2:")
    inner2()

if __name__ == "__main__":
  outer()

  
'''
Calling inner1:
statically scoped value of a: outer_a
statically scoped value of b: outer_b
statically scoped value of c: outer_c
statically scoped value of d: parameter_d
statically scoped value of e: inner3_e
dynamically scoped value of a: inner1_a
dynamically scoped value of b: inner1_b
dynamically scoped value of c: outer_c
dynamically scoped value of d: parameter_d
dynamically scoped value of e: inner3_e
Calling inner2:
statically scoped value of a: outer_a
statically scoped value of b: outer_b
statically scoped value of c: outer_c
statically scoped value of d: parameter_d
statically scoped value of e: inner3_e
dynamically scoped value of a: inner2_a
dynamically scoped value of b: inner2_b
dynamically scoped value of c: outer_c
dynamically scoped value of d: parameter_d
dynamically scoped value of e: inner3_e
'''
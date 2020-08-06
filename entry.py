
"""
Copyright (c) 2020 jcollinscastro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from algocomp import *


def setup(discriminant):
    L = isqrt(isqrt(-discriminant//4))
    info = {"D":discriminant, "L":L}
    cube = construct_nudupl_cube(2, 1, (1-discriminant)//8, L)
    return (cube, info)


def run(cube, info):
    """
    1) get the forms, and then just forget the original cube values
    2) reduce the form that needs squaring
    3) construct a new cube from scratch using a nudupl like algorithm
        which partially reduces the cube
    """
    a,b,c,d,e,f,g,h = cube

    # Because we are guaranteed (A1,B1,C1) = (A2,B2,C2)
    #   the equations show b=e, d=g.
    # Therefore we can slightly simplify the B3 form equations.
    assert b == e
    assert d == g

    # A3 = b*e - a*f
    A3 = b*b - a*f

    # B3 = -a*h + b*g - c*f + d*e
    B3 = -a*h - c*f + 2*b*d

    # C3 = d*g - c*h
    C3 = d*d - c*h

    A, B, C = reduce_form(A3, B3, C3)

    new_cube = construct_nudupl_cube(A, B, C, info["L"])

    if 0:
        # silly test, apply some arbitrary transformation to the cube
        new_cube = transform_cube(new_cube, 7,3,2,1)

    return new_cube


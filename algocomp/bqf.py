
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
from .gcd import xgcd
from .isqrt import isqrt
from .cost_tracking import (routine_tracking_start, routine_tracking_stop)
from .tracked_number import coerce_int as _int
from .int_div import exact_div


def reduce_form(a,b,c):
    """calculates reduced binary quadratic form"""
    a0,b0,c0 = a,b,c

    # -- normalize form --
    if c<a:
        """
        apply matrix
                |0 -1|
                |1  0|
        """
        a, b, c = c, -b, a
    if -a < b <= a:
        """
        This means that (a,b,c) is already reduced
        """
        return (a,b,c)

    tracking = routine_tracking_start("reduce_form", a, b, c)
    #http://mathonline.wikidot.com/reduced-binary-quadratic-forms
    n = (b + a) // (2*a) #  (quotient of b+a by 2a guarantees -a < b - 2*a*n < a) 
    # transform:  a, b, c = a, b - 2*a*n, c - b*n + a*n*n

    # This is the action under the matrix |1 -n|
    #                                     |0  1|
    an = a*n
    b = b - an
    c = c - n*b
    b = b - an

    routine_tracking_stop(tracking)

    return (a,b,c)


def nudupl(a,b,c, L=None):
    """
    calculates squared binary quadratic form composition
    returns reduced form

    from:
    'A Course in Computational Algebraic Number Theory', Henri Cohen
    Algorithm 5.4.8 (NUDUPL) page 243
    """

    # L should be precomputed, but for convenience/testing
    # added support for calculating it here
    if L is None:
        L = isqrt(isqrt(abs(b*b-4*a*c)//4))

    # -- Euclidean step --
    # u b + v a = d1 = gcd(b,a)
    d1,u,v = xgcd(b,a)
    A = a//d1
    B = b//d1
    C = (-c*u)%A
    C1 = A - C
    if C1 < C:
        C = -C1

    # -- Partial reduction --
    # PARTEUCL(A,C)
    v = 0
    d = A
    v2 = 1
    v3 = C
    z = 0
    while abs(v3) > L:
        q, t3 = divmod(d, v3)  # d = q v3 + t3
        t2 = v - q*v2
        # the following notes are not from the book
        # loop invariant: v2 d - v v3 = +/-A  (sign flips each step)
        #   v2 (q v3 + t3) - v v3 = +/-A
        #   v2 t3 - (v - q v2) v3 = +/-A
        #   v2 t3 - t2 v3 = +/-A
        #   t2 v3 - v2 t3 = -/+A  # sign flip
        #   v2' d' - v' v3' = -/+A
        v = v2
        d = v3
        v2 = t2
        v3 = t3
        z = z + 1
    if (z%2):
        v2 = -v2
        v3 = -v3
    #assert v2*d - v*v3 == A

    # -- Special case --
    if z == 0:
        g = exact_div(B*v3+c, d)
        a2 = d*d
        c2 = v3*v3
        b2 = b + (d+v3)*(d+v3) - a2 - c2
        c2 = c2 + g*d1
        return reduce_form(a2,b2,c2)

    # -- final computations --
    e = exact_div(c*v+B*d, A)
    g = exact_div(e*v2-B, v)
    b2 = e*v2 + v*g
    if d1 > 1:
        b2 = d1*b2
        v = d1*v
        v2 = d1*v2
    a2 = d*d
    c2 = v3*v3
    b2 = b2 + (d+v3)*(d+v3) - a2 - c2
    a2 = a2 + e*v
    c2 = c2 + g*v2

    return reduce_form(a2,b2,c2)


def test_nudupl():
    f = (20,7,1360)  # discriminant = -108751, class size = 231

    # expected answers calculated with pari-gp
    expected_answers = [
        (68, -7, 400),  # f0^2
        (161, 27, 170), # f0^4
        (10, 7, 2720),  # f0^8
        (100, 7, 272),  # f0^16
        (19, -9, 1432), # f0^32
        (98, 15, 278),  # f0^64
        (145, 17, 188), # f0^128
        (38, -9, 716),  # f0^256
        (160, 57, 175), # f0^512
        (118, -35, 233),# f0^1024
        (73, -47, 380), # f0^2048
    ]

    for i, answer in enumerate(expected_answers):
        f = nudupl(*f)
        if f != answer:
            raise Exception("failed on step {}, got:{} expected:{}".format(
                            i, f, answer))



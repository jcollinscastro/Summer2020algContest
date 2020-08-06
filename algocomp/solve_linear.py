
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
from .tracked_number import coerce_int as _int
from .gcd import xgcd
from .int_div import (exact_div, mod_min)


def solve_linear_x(a,b,c):
    """returns x with the minimum |x| such that a*x + b*y = c has a solution"""

    # Start by checking some special cases first
    if a==0:
        if b==0:
            assert c==0
            return (0,0)
        assert (_int(c) % _int(b)) == 0   # use _int to bypass cost for assert
        x = 0
        y = c//b
        return (x,y)

    if b==0:
        assert (_int(c) % _int(a)) == 0   # use _int to bypass cost for assert
        x = c//a
        y = 0
        return (x,y)

    # solve: a u + b v = g = gcd(a,b)
    g,u,v = xgcd(a,b)
    assert (_int(c) % _int(g))==0     # use _int to bypass cost for assert

    """
    given
        a u + b v = g = gcd(a,b)
    then
        a x + b y = c
    has the solution (with a freedom in 'n')
        x = u (c/g) + n b
        y = v (c/g) - n a

    using the freedom in n, we can get the minimal x
        -|b/2| < x <= |b/2|
    according to:
    x = (u c / g) % b
    if abs(x) > abs(b/2):  # basicly, but see mod_min for actual details
        x = x - b

    """

    if g == 1:
        x = mod_min(u*c, b) # note: b=0 already handled in special case
    else:
        x = mod_min(u*(c//g), b) # note: b=0 already handled in special case

    return x


def solve_linear(a,b,c):
    """return (x,y) such that a*x + b*y = c, with |x| minimized"""

    x = solve_linear_x(a,b,c)
    y = exact_div(c - a*x, b)
    return (x,y)



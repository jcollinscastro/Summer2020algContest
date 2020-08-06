
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
def exact_div(a, b):
    """
    performs integer division: a/b, with expectation that result is exact
    raises ValueError exception if b does not divide a
    """
    q, r = divmod(a, b)
    if r != 0:
        raise ValueError("dividend is not multiple of divisor")
    return q


def divmod_min(a, b):
    """
    return q,r such that a = qb + r, with minimum |r|
    """
    q, r = divmod(a, b)
    
    # we will want to adjust r if
    #   (|r| > |b/2|), which is equivalent to checking
    #   (|2r| > |b|),
    #   (|r| > |b| - |r|)
    # then using the fact that for python,
    # divmod will give |r| < |b|  and  r,b will have the same sign
    #   (|r| > |b - r|)
    diff = b - r
    if abs(r) > abs(diff):
        q = q + 1 
        r = -diff
    return q,r


def mod_min(a, b):
    """
    return r such that r = a (mod b), with minimum |r|
    """
    # like divmod_min, just skipping a single add
    r = (a % b)
    diff = b - r
    if abs(r) > abs(diff):
        r = -diff
    return r



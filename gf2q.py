#! /usr/bin/python2
# vim: set fileencoding = utf-8
import random
constant = {}
constant[64] = {}
constant[32] = {}
constant[16] = {}
constant[64]["GF2Q_HIBIT"] = 0x8000000000000000
constant[64]["GF2Q_MODULUS"] = 0x000000000000001B
constant[32]["GF2Q_HIBIT"] = 0x80000000
constant[32]["GF2Q_MODULUS"] = 0x000000AF
constant[16]["GF2Q_HIBIT"] = 0x8000
constant[16]["GF2Q_MODULUS"] = 0x002D

GF2Q_Q = 32
gf2q_zero = 0  # 0 in GF2Q
gf2q_unity = 1  # 1 in GF2Q
gf2q_x = 2  # x in GF2Q; because the modulus is primitive,
            # x is a generator for the multiplicative group


# Test if zero.
def gf2q_is_zero(x):
    return x == 0


# Test if unity.
def gf2q_is_unity(x):
    return x == 1


# Add two elements, return result.
def gf2q_add(x, y):
    """Multiply two elements in GF_2^q and return the result.

    >>> gf2q_add(74989, 75052)
    449
    """
    return x ^ y


def gf2q_mul(x, y):
    """Multiply two elements in GF_2^q and return the result.

    For instance, according to Sage, with k=GF(2^32,'c'), the following
    (k.fetch_int(74689)*k.fetch_int(44)).integer_representation()
    evaluates to 2697596, which, for the curious, is also:
    c^21 + c^19 + c^16 + c^13 + c^11 + c^8 + c^6 + c^5 + c^4 + c^3 + c^2
    >>> gf2q_mul(74989, 44)
    2697596L

    1 is unity element
    >>> gf2q_mul(74989, 0x1)
    74989L

    and ax, 0*x == 0
    >>> gf2q_mul(74989, 0x0)
    0L

    Finally, because GF_2^q is close under multiplication, even two big numbers
    must return something less than 2^q
    >>> gf2q_mul(2532981596, 1299567181)
    1692365615L
    """
    f = int(0)
    z = gf2q_zero
    for j in range(GF2Q_Q):
        if y & 1:
            z ^= x

        f = x & constant[GF2Q_Q]['GF2Q_HIBIT']
        x <<= 1
        if f:
            x ^= constant[GF2Q_Q]['GF2Q_MODULUS']

        y >>= 1

    return z % (1 << GF2Q_Q)


def gf2q_rand():
    """Returns a pseudo random element of GF_2^q.

    All elements must be in the field
    >>> l=[gf2q_rand() for i in range(1000)];min(l)>= 0
    True
    >>> l=[gf2q_rand() for i in range(1000)];max(l)<= (1 << GF2Q_Q)-1
    True

    And we may expect that they don't repeat themselves to often.
    >>> l=[gf2q_rand() for i in range(2000)]; gf2q_rand() not in l
    True
    """
    if GF2Q_Q % 8 != 0:
        raise ValueError("gf2q_rand: GF2Q_Q must be a multiple of 8")
    z = gf2q_zero
    # the value I get on my 32-bits linux
    RAND_MAX = 2*((1 << 30)-1)+1
    for j in range(1, GF2Q_Q/8):
        z ^= (random.randint(0, RAND_MAX) % 0xFF)
        z <<= 8

    z ^= (random.randint(0, RAND_MAX) % 0xFF)
    return z

if __name__ == '__main__':
    import doctest
    doctest.testmod()

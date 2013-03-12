#! /usr/bin/python2
# vim: set fileencoding=utf-8
import random
constant = {}
constant[64]={}
constant[32]={}
constant[16]={}
constant[64]["GF2Q_HIBIT"] = 0x8000000000000000L
constant[64]["GF2Q_MODULUS"] = 0x000000000000001BL
constant[32]["GF2Q_HIBIT"] = 0x80000000
constant[32]["GF2Q_MODULUS"] = 0x000000AF
constant[16]["GF2Q_HIBIT"] = 0x8000
constant[16]["GF2Q_MODULUS"] = 0x002D

GF2Q_Q = 32
gf2q_zero  = 0; # 0 in GF2Q
gf2q_unity = 1; # 1 in GF2Q
gf2q_x     = 2; # x in GF2Q; because the modulus is primitive, x is a generator for the multiplicative group

# Test if zero.
def gf2q_is_zero(x):
    return x == 0

# Test if unity.
def gf2q_is_unity(x):
    return x == 1

# Add two elements, return result.
def gf2q_add(x, y):
    return x^y

# Multiply two elements, return result.
def gf2q_mul(x, y):
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

    return z

# Returns pseudorandom element. Seed with srand().
# compare C rand() and randint()
def gf2q_rand():
    if GF2Q_Q % 8 != 0:
        raise ValueError("gf2q_rand: GF2Q_Q must be a multiple of 8")
    z = gf2q_zero
    for j in range(GF2Q_Q/8):
        z ^= (random.randint(0,1<<63) % 0xFF)
        z <<= 8

    z ^= (random.randint(0,1<<63) % 0xFF)
    return z

if __name__ == '__main__':
    o=0x1
    x = 0x124ed;
    y = 0x1252c;
    z = 0x2c;
    print 'z==0 {}'.format(gf2q_is_zero(0x0))
    print 'o==1 {}'.format(gf2q_is_unity(o))
    print 'x+y {} (0x1c1)'.format(hex(gf2q_add(x,y)))
    print 'x*z {} (0x29297c)'.format(hex(gf2q_mul(x,z)))
    print 'r {}'.format(gf2q_rand())

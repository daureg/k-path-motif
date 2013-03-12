#ifndef GUARD_GF2Q__
#define GUARD_GF2Q__

/************* Arithmetic in the finite field GF(2^q) for q = 16, 32, or 64. */

#include <stdlib.h>   /* get rand() */
#include <stdbool.h>   /* get bool type */

/*
 * CAVEAT 1: We assume the field element fits in one word.
 *
 * CAVEAT 2: Check that lengths of "long int", "int" & "short int" below
 *           match your architecture.
 */

/*
 * Some primitive polynomials (see GF2Q_MODULUS below) for field construction:
 *
 * degree 16: x^16 + x^5 + x^3 + x^2 + 1
 * degree 32: x^32 + x^7 + x^5 + x^3 + x^2 + x + 1
 * degree 64: x^64 + x^4 + x^3 + x + 1
 *
 * For a list of primitive polynomials, see e.g.:
 *
 * http://www.ams.org/journals/mcom/1962-16-079/S0025-5718-1962-0148256-1/S0025-5718-1962-0148256-1.pdf
 *
 */

#define GF2Q_Q 32 /* must be one of 16, 32, or 64 */

#if GF2Q_Q==64
typedef unsigned long int   gf2q_t;   /* Represent GF(2^64) using 64 bits */
#define GF2Q_Q              64
#define GF2Q_HIBIT          0x8000000000000000L
#define GF2Q_MODULUS        0x000000000000001BL
#endif

#if GF2Q_Q==32
typedef unsigned int        gf2q_t;   /* Represent GF(2^32) using 32 bits */
#define GF2Q_Q              32
#define GF2Q_HIBIT          0x80000000
#define GF2Q_MODULUS        0x000000AF
#endif

#if GF2Q_Q==16
typedef unsigned short int  gf2q_t;   /* Represent GF(2^16) using 16 bits */
#define GF2Q_Q              16
#define GF2Q_HIBIT          0x8000
#define GF2Q_MODULUS        0x002D
#endif

const static gf2q_t gf2q_zero  = 0; /* 0 in GF2Q */
const static gf2q_t gf2q_unity = 1; /* 1 in GF2Q */
const static gf2q_t gf2q_x     = 2; /* x in GF2Q; because the modulus is primitive,
                        * x is a generator for the multiplicative group */

/* Test if zero. */
bool gf2q_is_zero(gf2q_t x);
/* Test if unity. */
bool gf2q_is_unity(gf2q_t x);
/* Add two elements, return result. */
gf2q_t gf2q_add(const gf2q_t x, const gf2q_t y);
/* Multiply two elements, return result. */
gf2q_t gf2q_mul(gf2q_t x, gf2q_t y);
/* Returns pseudorandom element. Seed with srand(). */
gf2q_t gf2q_rand(void);

#endif

#include "gf2q.h"

bool gf2q_is_zero(gf2q_t x) {
	return x == 0;
}

bool gf2q_is_unity(gf2q_t x) {
	return x == 1;
}

gf2q_t gf2q_add(gf2q_t x, gf2q_t y) {
	return x^y;
}

gf2q_t gf2q_mul(gf2q_t x, gf2q_t y) {
	int j;
	gf2q_t f;
	gf2q_t z = gf2q_zero;

	for (j = 0; j < GF2Q_Q; j++) {
		if (y & 1) {
			z ^= x;
		}

		f = x & GF2Q_HIBIT;
		x <<= 1;

		if (f) {
			x ^= GF2Q_MODULUS;
		}

		y >>= 1;
	}

	return z;
}

gf2q_t gf2q_rand(void) {
#if !(GF2Q_Q % 8 == 0)
#error "gf2q_rand: GF2Q_Q must be a multiple of 8"
#endif
	gf2q_t z = gf2q_zero;
	int j;

	for (j = 1; j < GF2Q_Q/8; j++) {
		z ^= (rand() % 0xFF);
		z <<= 8;
	}

	z ^= (rand() % 0xFF);
	return z;
}

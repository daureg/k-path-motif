#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <check.h>
#include "gf2q.h"

char* error;
void setup(void) {
	error = malloc(256*sizeof(char));
}
void teardown(void) {
	free(error);
}

START_TEST(test_addition) {
	gf2q_t x = 0x124ed;
	gf2q_t y = 0x1252c;
	gf2q_t great = 0xffffffec;
	gf2q_t small = 0xff;
	fail_unless(gf2q_add(x,y)==0x1c1, "addition in F_q");
	fail_unless(gf2q_add(great, small)==0xffffff13, "addition in F_q");
	fail_unless(gf2q_is_unity(gf2q_add(1,0)), "0 is identity element for + in F_q");
	fail_unless(gf2q_is_zero(gf2q_add(1,1)), "F_q has caracteristic 2");
}
END_TEST

START_TEST(test_multiplication) {
	gf2q_t x = 0x124ed;
	gf2q_t y = 0x2c;
	gf2q_t res = 0x29297c; /* according to Sage, with k=GF(2^32,'c') and
				  res=hex((k.fetch_int(x)*k.fetch_int(y)).integer_representation())
				  For the curious, this is also:
				  c^21 + c^19 + c^16 + c^13 + c^11 + c^8 + c^6 + c^5 + c^4 + c^3 + c^2
				  */
	fail_unless(gf2q_mul(x,y)==res, "multiplication in F_q");
	fail_unless(gf2q_mul(x,1)==x, "1 is identity element for * in F_q");
	fail_unless(gf2q_is_zero(gf2q_mul(x,gf2q_zero)), "0*x==0");
}
END_TEST

Suite* motif_suite(void) {
	Suite* s = suite_create("k-motif path");
	TCase* tc_field = tcase_create("Galois field");
	tcase_add_checked_fixture(tc_field, setup, teardown);
	tcase_add_test(tc_field, test_addition);
	tcase_add_test(tc_field, test_multiplication);
	suite_add_tcase(s, tc_field);
	return s;
}

int main(void) {
	int number_failed;
	Suite* s = motif_suite();
	SRunner* sr = srunner_create(s);
	srunner_run_all(sr, CK_ENV);
	number_failed = srunner_ntests_failed(sr);
	srunner_free(sr);
	return (number_failed == 0) ? EXIT_SUCCESS : EXIT_FAILURE;
}

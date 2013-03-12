#include <stdlib.h>
#include <stdio.h>
#include <check.h>

char* error;
void setup(void) {
	error = malloc(256*sizeof(char));
}
void teardown(void) {
	free(error);
}

START_TEST(test_always_true) {
	fail_unless(0==0, "how can you fail this!");
}
END_TEST

Suite* motif_suite(void) {
	Suite* s = suite_create("k-motif path");
	TCase* tc_field = tcase_create("Galois field");
	tcase_add_checked_fixture(tc_field, setup, teardown);
	tcase_add_test(tc_field, test_always_true);
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

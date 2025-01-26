#include <iostream>

int main(int argc, char *argv[]) {
  check_valid_firmware();
  get_tests();
  test_firmware();
  print_results();

  return 0;
}

// expect-fail: x is modified twice without sequencing
// passes-without: -Werror
#include <iostream>

int main()
{
    int x{1};
    std::cout << x++ + x++ << "\n";
    return 0;
}

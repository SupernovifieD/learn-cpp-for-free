// expect-fail: the literal 'ab' has two characters, and its value is not
// portable passes-without: -Werror
#include <iostream>

int main()
{
    int code{'ab'};
    std::cout << code << "\n";
    return 0;
}

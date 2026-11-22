// expect-fail: 'ab' has two characters and a compiler-defined value
// passes-without: -Werror
#include <iostream>

int main()
{
    int code{'ab'};
    std::cout << code << "\n";
    return 0;
}

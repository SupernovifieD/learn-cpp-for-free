// expect-fail: the result of the expression is thrown away
// passes-without: -Werror
#include <iostream>

int main()
{
    int width{5};
    width * 2;
    std::cout << width << "\n";
    return 0;
}

// expect-fail: the compiler sees that 2147483647 + 1 does not fit in an int
// passes-without: -Werror
#include <iostream>

int main()
{
    int next{2147483647 + 1};
    std::cout << next << "\n";
    return 0;
}

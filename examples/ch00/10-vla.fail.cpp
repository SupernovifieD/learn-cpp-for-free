// expect-fail: variable-length arrays are not standard C++
// passes-without: -pedantic-errors -Werror
#include <iostream>

int main()
{
    int size{};
    std::cin >> size;
    int numbers[size];
    numbers[0] = 1;
    return 0;
}

// expect-fail: the discarded right operand has no effect
// passes-without: -Werror
#include <iostream>

int main()
{
    int a{4};
    int b{9};
    int result{};

    result = a, b;
    std::cout << result << "\n";
    return 0;
}

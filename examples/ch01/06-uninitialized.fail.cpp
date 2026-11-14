// expect-fail: the variable is read before it has a value
// passes-without: -Werror
#include <iostream>

int main()
{
    int visitors;
    std::cout << "visitors: " << visitors << "\n";
    return 0;
}

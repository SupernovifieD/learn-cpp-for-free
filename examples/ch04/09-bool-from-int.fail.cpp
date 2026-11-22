// expect-fail: a brace initializer does not accept the integer 2 for a bool
#include <iostream>

int main()
{
    bool flag{2};
    std::cout << flag << "\n";
    return 0;
}

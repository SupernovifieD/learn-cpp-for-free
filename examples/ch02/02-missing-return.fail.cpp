// expect-fail: a function that returns an int ends without returning one
// passes-without: -Werror
#include <iostream>

int getFive()
{
    std::cout << "Working out the number...\n";
}

int main()
{
    std::cout << getFive() << "\n";
    return 0;
}

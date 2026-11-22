// expect-fail: assigning a double to an int silently drops the fraction
// passes-without: -Werror
#include <iostream>

int main()
{
    double price{4.75};
    int whole{0};
    whole = price;
    std::cout << whole << "\n";
    return 0;
}

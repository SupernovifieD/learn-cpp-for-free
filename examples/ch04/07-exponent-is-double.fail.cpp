// expect-fail: a literal written with an exponent is a double, not an int
#include <iostream>

int main()
{
    int copies{1e3};
    std::cout << copies << "\n";
    return 0;
}

// expect-fail: the name is not declared
#include <iostream>

int main()
{
    std::cout << missing << "\n";
    return 0;
}

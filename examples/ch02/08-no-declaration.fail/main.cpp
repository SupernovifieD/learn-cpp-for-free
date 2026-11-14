// expect-fail: square is used, but this file never declares it
#include <iostream>

int main()
{
    std::cout << "7 squared is " << square(7) << "\n";
    return 0;
}

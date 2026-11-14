// expect-fail: square is declared, but no file of the build defines it
#include <iostream>

int square(int number);

int main()
{
    std::cout << "7 squared is " << square(7) << "\n";
    return 0;
}

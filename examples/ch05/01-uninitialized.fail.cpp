// expect-fail: a const variable must be given its value when it is defined
#include <iostream>

int main()
{
    const int pitchFee;
    std::cout << pitchFee << "\n";
    return 0;
}

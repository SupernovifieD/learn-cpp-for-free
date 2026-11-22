// expect-fail: a const variable cannot be changed after its definition
#include <iostream>

int main()
{
    const int pitchFee{25};
    pitchFee = 30;
    std::cout << pitchFee << "\n";
    return 0;
}

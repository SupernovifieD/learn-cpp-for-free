// expect-fail: const on a returned int has no effect, and the compiler says so
// passes-without: -Werror
#include <iostream>

const int pitchFee()
{
    return 25;
}

int main()
{
    std::cout << pitchFee() << "\n";
    return 0;
}

// expect-fail: the value 40000 does not fit in a 16-bit short
#include <iostream>

int main()
{
    short stock{40000};
    std::cout << stock << "\n";
    return 0;
}

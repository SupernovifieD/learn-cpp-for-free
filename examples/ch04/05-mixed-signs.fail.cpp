// expect-fail: a signed value is silently converted to unsigned in a
// calculation passes-without: -Werror
#include <iostream>

int main()
{
    unsigned int copies{10};
    int returned{-15};
    unsigned int total{copies + returned};
    std::cout << total << "\n";
    return 0;
}

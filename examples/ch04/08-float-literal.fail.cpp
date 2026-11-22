// expect-fail: the double literal 3.14 is converted to a float
// passes-without: -Werror
#include <iostream>

int main()
{
    float ratio{3.14};
    std::cout << ratio << "\n";
    return 0;
}

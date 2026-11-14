// expect-fail: a name cannot contain a space
#include <iostream>

int main()
{
    int first place{2};
    std::cout << "position: " << first place << "\n";
    return 0;
}

// expect-fail: add is called before the compiler has seen it
#include <iostream>

int main()
{
    std::cout << add(2, 3) << "\n";
    return 0;
}

int add(int left, int right)
{
    return left + right;
}

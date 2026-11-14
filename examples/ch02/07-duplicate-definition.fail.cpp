// expect-fail: the function add is defined twice in the same file
#include <iostream>

int add(int left, int right)
{
    return left + right;
}

int add(int left, int right)
{
    return right + left;
}

int main()
{
    std::cout << add(2, 3) << "\n";
    return 0;
}

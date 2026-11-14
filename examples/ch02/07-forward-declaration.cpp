#include <iostream>

int add(int left, int right);

int main()
{
    std::cout << add(2, 3) << "\n";
    return 0;
}

int add(int left, int right)
{
    return left + right;
}

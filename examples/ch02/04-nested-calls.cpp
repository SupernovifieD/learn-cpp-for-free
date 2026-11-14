#include <iostream>

int addOne(int number)
{
    return number + 1;
}

int twice(int number)
{
    return number * 2;
}

int main()
{
    std::cout << twice(addOne(4)) << "\n";
    std::cout << addOne(twice(4)) << "\n";
    return 0;
}

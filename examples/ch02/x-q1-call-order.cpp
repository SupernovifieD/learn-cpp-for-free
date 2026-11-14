#include <iostream>

int addOne(int number)
{
    return number + 1;
}

int twice(int number)
{
    return number * 2;
}

void show(int value)
{
    std::cout << value << "\n";
}

int main()
{
    int start{3};
    show(start);
    show(addOne(start));
    show(twice(addOne(start)));
    show(start);
    return 0;
}

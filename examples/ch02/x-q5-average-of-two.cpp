#include <iostream>

int average(int left, int right)
{
    return (left + right) / 2;
}

int main()
{
    int first{};
    int second{};

    std::cout << "Enter two numbers: ";
    std::cin >> first >> second;

    std::cout << "Average: " << average(first, second) << "\n";
    return 0;
}

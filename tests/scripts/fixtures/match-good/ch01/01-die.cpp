#include <iostream>
#include <random>

int main()
{
    std::random_device source{};
    std::uniform_int_distribution<int> die{1, 6};
    std::cout << die(source) << "\n";
    return 0;
}

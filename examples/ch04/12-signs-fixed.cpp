#include <iostream>

int main()
{
    unsigned int copies{10};
    int returned{-15};
    int total{static_cast<int>(copies) + returned};
    unsigned int wrapped{static_cast<unsigned int>(returned)};

    std::cout << "Total: " << total << "\n";
    std::cout << "Returned as unsigned: " << wrapped << "\n";
    return 0;
}

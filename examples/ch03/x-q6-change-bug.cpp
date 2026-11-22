#include <iostream>

int changeDue(int paid, int cost)
{
    return paid - cost;
}

int main()
{
    int paid{50};
    int cost{37};
    std::cout << "Change: " << changeDue(cost, paid) << "\n";
    return 0;
}

#include <iostream>

void printScore(int round, int points)
{
    std::cout << "Round " << round << ": " << points << " points\n";
}

int main()
{
    printScore(1, 10);
    printScore(2, 25);
    printScore(3, 40);
    return 0;
}

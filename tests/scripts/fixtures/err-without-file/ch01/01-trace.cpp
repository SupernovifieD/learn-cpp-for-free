#include <iostream>

void step(int number)
{
    std::cerr << "[debug] step " << number << "\n";
    std::cout << "step " << number << " done\n";
}

int main()
{
    step(1);
    step(2);
    return 0;
}

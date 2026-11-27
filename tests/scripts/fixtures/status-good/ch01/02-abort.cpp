#include <cstdlib>
#include <iostream>

int main()
{
    std::cout << "Stopping abnormally\n";
    std::cout.flush();
    std::abort();
}

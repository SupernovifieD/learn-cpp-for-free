#include <iostream>
#include <string>

int main()
{
    std::cout << "Number of guests: ";
    int guests{};
    std::cin >> guests;

    std::cout << "Trip name: ";
    std::string trip{};
    std::getline(std::cin >> std::ws, trip);

    std::cout << "Trip: " << trip << " for " << guests << " guests\n";
    return 0;
}

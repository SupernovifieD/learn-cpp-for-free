#include <cstddef>
#include <iostream>
#include <string>

int main()
{
    std::string first{"Noor"};
    std::string last{"Haddad"};

    std::string full{first + " " + last};
    std::cout << "Full name: " << full << "\n";

    std::size_t size{full.length()};
    std::cout << "Characters: " << size << "\n";

    first = "Samir";
    std::cout << "After the assignment: " << first << " " << last << "\n";
    return 0;
}

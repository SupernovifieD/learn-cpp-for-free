#include <iostream>
#include <string>
#include <string_view>

void printLine(std::string_view label, std::string_view value)
{
    std::cout << label << ": " << value << "\n";
}

int main()
{
    std::string city{"Lisbon"};

    printLine("Destination", city);
    printLine("Transport", "train");
    return 0;
}

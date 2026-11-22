#include <iostream>
#include <string>
#include <string_view>

void printLabel(std::string_view label)
{
    std::cout << "Label: " << label << " (" << label.length()
              << " characters)\n";
}

int main()
{
    std::string title{"Packing list"};
    std::string_view heading{title};

    printLabel("Tent");
    printLabel(title);
    printLabel(heading);
    return 0;
}

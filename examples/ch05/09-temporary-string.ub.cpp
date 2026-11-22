// undefined-behavior: the view refers to a temporary string that is gone
#include <iostream>
#include <string>
#include <string_view>

std::string makeLabel()
{
    return std::string{"Label for the shelf in the corner of the reading room"};
}

int main()
{
    std::string_view label{makeLabel()};
    std::cout << label << "\n";
    return 0;
}

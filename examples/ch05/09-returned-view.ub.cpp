// undefined-behavior: returns a view of a local string that is destroyed
#include <iostream>
#include <string>
#include <string_view>

std::string_view shelfName()
{
    std::string name{
        "A long name that does not fit in the small string buffer"};
    return name;
}

int main()
{
    std::cout << shelfName() << "\n";
    return 0;
}

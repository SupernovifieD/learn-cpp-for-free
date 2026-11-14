#include <iostream>

int main()
{
    std::cout << "A string literal cannot continue on the next line, "
                 "but neighboring literals are joined.\n";
    std::cout << "Spaces    inside    a literal    are    kept.\n";
    return 0;
}

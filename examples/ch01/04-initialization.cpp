#include <iostream>

int main()
{
    int copyForm = 5;
    int directForm(6);
    int braceForm{7};
    int emptyBraces{};

    std::cout << "copy form: " << copyForm << "\n";
    std::cout << "direct form: " << directForm << "\n";
    std::cout << "brace form: " << braceForm << "\n";
    std::cout << "empty braces: " << emptyBraces << "\n";

    braceForm = 70;
    std::cout << "brace form after assignment: " << braceForm << "\n";
    return 0;
}

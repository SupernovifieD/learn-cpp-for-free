// expect-fail: a brace initializer rejects a value that would lose its fraction
#include <iostream>

int main()
{
    int wholeNumber{4.5};
    std::cout << wholeNumber << "\n";
    return 0;
}

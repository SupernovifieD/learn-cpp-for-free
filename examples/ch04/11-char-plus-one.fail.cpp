// expect-fail: letter + 1 is an int, and a char cannot hold it without a cast
#include <iostream>

int main()
{
    char letter{'A'};
    char next{letter + 1};
    std::cout << next << "\n";
    return 0;
}

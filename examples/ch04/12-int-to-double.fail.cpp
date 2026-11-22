// expect-fail: a brace initializer does not accept an int variable for a double
#include <iostream>

int main()
{
    int cups{3};
    double total{cups};
    std::cout << total << "\n";
    return 0;
}

#include <iostream>

int main()
{
    double wrong{1 / 2};
    double right{1.0 / 2};

    std::cout << "Wrong: " << wrong << "\n";
    std::cout << "Right: " << right << "\n";
    return 0;
}

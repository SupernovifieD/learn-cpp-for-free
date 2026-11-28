#include <iostream>

int main()
{
    int value{5};

    int expressionValue{++value};
    std::cout << "++x " << value << " " << expressionValue << "\n";

    expressionValue = value++;
    std::cout << "x++ " << value << " " << expressionValue << "\n";

    expressionValue = --value;
    std::cout << "--x " << value << " " << expressionValue << "\n";

    expressionValue = value--;
    std::cout << "x-- " << value << " " << expressionValue << "\n";
    return 0;
}

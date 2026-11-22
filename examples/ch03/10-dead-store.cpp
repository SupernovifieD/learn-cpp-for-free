#include <iostream>

int main()
{
    int tickets{4};
    int price{15};
    int cost{tickets * price};
    std::cout << "Cost: " << cost << "\n";
    tickets = 5;
    return 0;
}

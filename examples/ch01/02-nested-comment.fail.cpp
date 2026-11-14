// expect-fail: the first */ ends the comment, so the last */ is stray text
#include <iostream>

int main()
{
    /* Switch off both lines:
    std::cout << "One\n";
    std::cout << "Two\n"; /* the second one */
    return 0;
    */
}

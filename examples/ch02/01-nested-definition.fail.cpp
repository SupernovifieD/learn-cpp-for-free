// expect-fail: a function cannot be defined inside another function
#include <iostream>

int main()
{
    void sayHi()
    {
        std::cout << "Hi\n";
    }

    sayHi();
    return 0;
}

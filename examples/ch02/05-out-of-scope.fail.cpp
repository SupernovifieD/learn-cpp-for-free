// expect-fail: a local variable cannot be used outside its function
#include <iostream>

void prepare()
{
    int readyCount{1};
    std::cout << "ready items: " << readyCount << "\n";
}

int main()
{
    prepare();
    std::cout << readyCount << "\n";
    return 0;
}

// expect-fail: the condition assigns 5 to level instead of comparing it
// passes-without: -Werror
#include <iostream>

int main()
{
    int level{2};
    if (level = 5)
    {
        std::cout << "Level five\n";
    }
    return 0;
}

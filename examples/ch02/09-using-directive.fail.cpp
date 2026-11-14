// expect-fail: cout now means two things, so the name is ambiguous
#include <iostream>

using namespace std;

int cout{0};

int main()
{
    cout << "Hello\n";
    return 0;
}

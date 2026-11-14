// expect-fail: add is declared but never defined, so linking fails
int add(int left, int right);

int main()
{
    return add(1, 2);
}

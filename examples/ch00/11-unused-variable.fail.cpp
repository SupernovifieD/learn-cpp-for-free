// expect-fail: an unused variable is only an error when warnings are errors
// passes-without: -Werror
int main()
{
    int unused{0};
    return 0;
}

#include <iostream>
#include <vector>

class Foo {
  public:
    void bar() {
      std::cout << "Hello" << std::endl;
    }
    double * test() {
      return asdf.data();
    }

    std::vector<double> asdf = { 1.0, 2.0, 3.0, 4.0, };
};

extern "C" {
  Foo* Foo_new() { return new Foo(); }
  void Foo_bar(Foo* foo) { foo->bar(); }
  double * Foo_test(Foo* foo) { return foo->test(); }
}

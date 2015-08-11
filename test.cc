#include <iostream>
#include <string>

namespace myNamespace {

class myClass {
  public:
    void f();

  private:
    int myMember;
};

} // ns

namespace {

struct myStruct {
  myNamespace::myClass myMember;

  void g() { }
};

} // ns


int main() {
  int decl;
  int def = 0;

  myNamespace::myClass a;
  myStruct b;
}

#include <iostream>
#include <vector>
#include <Eigen/Dense>

using Vector = Eigen::Vector3d;

class SimpleCircle {
public:

  double* get_control(size_t n) {
    if (n == 0) return nullptr;
    control.resize(n);

    control[0] = Vector({1., 1., 1.});
    control[1] = Vector({2., 2., 2.});
    control[2] = Vector({3., 3., 3.});

    return control[0].data();
  }

private:

  std::vector<Vector> control;

};

extern "C" {
  SimpleCircle* SC_construct() { return new SimpleCircle(); }
  double * SC_get_control(SimpleCircle* sc, size_t n) { return sc->get_control(n); }
}

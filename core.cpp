#include <iostream>
#include <vector>
#include <Eigen/Dense>

using Vector = Eigen::Vector3d;

class SimpleCircle {
public:

  void set_degree(size_t n) {
    degree = n;
  }

  double* get_control(size_t n) {
    if (n == 0) return nullptr;
    control.resize(n);

    return control[0].data();
  }

  double* get_samples(size_t n) {
    if (n == 0) return nullptr;
    samples.resize(n);

    compute_samples();

    return samples[0].data();
  }

private:

  size_t degree;

  std::vector<Vector> samples;
  std::vector<Vector> control;

  void compute_samples() {
    for (size_t i = 0; i < samples.size(); i++) {
      // actually compute something
    }
  }

};

extern "C" {
  SimpleCircle* SC_construct() { return new SimpleCircle(); }
  void SC_set_degree(SimpleCircle* sc, size_t n) { sc->set_degree(n); }
  double * SC_get_control(SimpleCircle* sc, size_t n) { return sc->get_control(n); }
  double * SC_get_samples(SimpleCircle* sc, size_t n) { return sc->get_samples(n); }
}

#include <iostream>
#include <vector>
#include <math.h>
#include <Eigen/Dense>

#define PI 3.14159265

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
      double t = static_cast<double>(i)/static_cast<double>(samples.size());

      samples[i][0] = t;
      samples[i][1] = sin(2.0*PI*t);
      samples[i][2] = 2.0*cos(2.0*PI*t);
    }
  }

};

extern "C" {
  SimpleCircle* SC_construct() { return new SimpleCircle(); }
  void SC_set_degree(SimpleCircle* sc, size_t n) { sc->set_degree(n); }
  double * SC_get_control(SimpleCircle* sc, size_t n) { return sc->get_control(n); }
  double * SC_get_samples(SimpleCircle* sc, size_t n) { return sc->get_samples(n); }
}

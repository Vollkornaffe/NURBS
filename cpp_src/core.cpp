#include <iostream>
#include <vector>
#include <math.h>
#include <Eigen/Dense>
#include <functional>

#define PI 3.14159265

using Vector = Eigen::Vector3d;

template<typename T>
struct CVector {

  static inline size_t modulo( int value, unsigned m) {
    int mod = value % (int)m;
      if (value < 0) mod += m;
    return mod;
  }

  inline T& operator[](int i) {
    return vector[modulo(i, vector.size())];
  }

  std::vector<T> vector;
};

class SimpleCircle {
public:

  SimpleCircle(size_t degree, size_t numControl, size_t numSamples)
  : degree(degree), numControl(numControl), numSamples(numSamples) {

    if (numControl < 3 || degree+1 > numControl) {
      throw std::invalid_argument("Number of controlpoints MUST be larger or equal degree.");
    }

    if (numSamples < 1) {
      throw std::invalid_argument("At least one sample.");
    }

    intervals.vector.resize(numControl, 1.0/static_cast<double>(numControl));
    control.vector.resize(numControl);

    samples.resize(numSamples);

  }

  double* get_control() {
    return control.vector[0].data();
  }

  double* get_intervals() {
    return intervals.vector.data();
  }

  double* get_samples() {
    compute_samples();
    return samples[0].data();
  }

private:

  // Most of this algorithm is inspired by The NURBS Book, Algorithm A2.2
  void compute_samples() {

    size_t i = 0;
    double offset;
    std::vector<double> left(degree+1);
    std::vector<double> right(degree+1);
    std::vector<double> bases(degree+1);
    for (size_t s = 0; s < numSamples; s++) {

      // convert to parameter t
      double t = static_cast<double>(s)/static_cast<double>(numSamples);

      // advance interval if needed
      // with safeguard against floating point errors
      if (offset + intervals[i] < t && i < numControl-1) {
        offset += intervals[i];
        i++;
      }

      left[0] = t - offset - intervals[i];
      right[0] = offset - t;
      for (size_t j = 1; j < degree+1; j++) {
        left[j] = left[j-1] + intervals[(int)i - (int)j + 1];
        right[j] = right[j-1] + intervals[(int)i + (int)j - 1];
      }

      bases[0] = 1.0;
      for (size_t j = 1; j <= degree; j++) {
        double saved = 0.0;
        for (size_t r = 0; r < j; r++) {
          double temp = bases[r] / (right[r+1] + left[j-r]);
          bases[r] = saved + right[r+1] * temp;
          saved = left[j-r] * temp;
        }
        bases[j] = saved;
      }

      samples[s] = Vector::Zero();
      for (size_t j = 0; j <= degree; j++) {
        samples[s] += bases[j] * control[(int)i - (int)degree + (int)j];
      }
    }
  }

  size_t degree;
  size_t numControl;
  size_t numSamples;

  CVector<double> intervals;
  CVector<Vector> control;
  std::vector<Vector> samples;

};

extern "C" {
  SimpleCircle* SC_construct(size_t degree, size_t numControl, size_t numSamples) {
    try {
      return new SimpleCircle(degree, numControl, numSamples);
    } catch (...)  {
      return nullptr;
    }
  }
  double * SC_get_intervals(SimpleCircle* sc) { return sc->get_intervals(); }
  double * SC_get_control(SimpleCircle* sc) { return sc->get_control(); }
  double * SC_get_samples(SimpleCircle* sc) { return sc->get_samples(); }
}

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
  inline T const& operator[](int i) const {
    return vector[modulo(i, vector.size())];
  }

  std::vector<T> vector;
};

inline void advance(
  CVector<double> const & intervals,
  double const & t,
  size_t const & degree,
  size_t & i,
  double & offset,
  std::vector<double> & left,
  std::vector<double> & right
) {

  // advance interval if needed
  // with safeguard against floating point errors
  if (offset + intervals[i] < t && i < intervals.vector.size()-1) {
    offset += intervals[i];
    i++;
  }

  left[0] = t - offset - intervals[i];
  right[0] = offset - t;
  for (size_t j = 1; j < degree+1; j++) {
    left[j] = left[j-1] + intervals[(int)i - (int)j + 1];
    right[j] = right[j-1] + intervals[(int)i + (int)j - 1];
  }

}

inline void compute_bases(
  CVector<double> const & intervals,
  size_t const & degree,
  size_t const & i,
  std::vector<double> const & left,
  std::vector<double> const & right,
  std::vector<double> & bases
) {

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

}

class CyclicCurve {
public:

  CyclicCurve(size_t degree, size_t numControl, size_t numSamples)
  : degree(degree), numControl(numControl), numSamples(numSamples) {

    if (numControl < 3 || degree+1 > numControl) {
      throw std::invalid_argument("Number of controlpoints MUST be larger or equal degree.");
    }

    if (numSamples < 1) {
      throw std::invalid_argument("At least one sample.");
    }

    intervals.vector.resize(numControl, 1.0/static_cast<double>(numControl));
    control.vector.resize(numControl);

    samples.resize(numSamples, Vector::Zero());

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
    double offset = 0.0;
    std::vector<double> left(degree+1);
    std::vector<double> right(degree+1);
    std::vector<double> bases(degree+1);
    for (size_t s = 0; s < numSamples; s++) {

      // convert to parameter t
      double t = static_cast<double>(s)/static_cast<double>(numSamples);

      advance(intervals, t, degree, i, offset, left, right);

      compute_bases(intervals, degree, i, left, right, bases);

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

class CyclicSurface {
public:

  CyclicSurface(
    size_t u_degree, size_t v_degree,
    size_t u_numControl, size_t v_numControl,
    size_t u_numSamples, size_t v_numSamples)
  : u_degree(u_degree), v_degree(v_degree),
    u_numControl(u_numControl), v_numControl(v_numControl),
    u_numSamples(u_numSamples), v_numSamples(v_numSamples) {

    if (u_numControl < 3 || u_degree+1 > u_numControl
    ||  v_numControl < 3 || v_degree+1 > v_numControl) {
      throw std::invalid_argument("Number of controlpoints MUST be larger or equal degree.");
    }

    if (u_numSamples < 1 || v_numSamples < 1) {
      throw std::invalid_argument("At least one sample.");
    }

    u_intervals.vector.resize(u_numControl, 1.0/static_cast<double>(u_numControl));
    v_intervals.vector.resize(v_numControl, 1.0/static_cast<double>(v_numControl));

    uv_control.vector.resize(u_numControl);
    for (auto& cvector : uv_control.vector) {
      cvector.vector.resize(v_numControl);
    }

    uv_samples.resize(u_numSamples*v_numSamples, Vector::Zero());

  }

  double* get_control(size_t n) {
    return uv_control.vector[n].vector[0].data();
  }

  double* get_u_intervals() {
    return u_intervals.vector.data();
  }
  double* get_v_intervals() {
    return v_intervals.vector.data();
  }

  double* get_samples() {
    compute_samples();
    return uv_samples[0].data();
  }


private:

  // Most of this algorithm is inspired by The NURBS Book, Algorithm A2.2
  void compute_samples() {

    size_t s = 0;
    size_t u_i = 0;
    double u_offset = 0.0;
    std::vector<double> u_left(u_degree+1);
    std::vector<double> v_left(v_degree+1);
    std::vector<double> u_right(u_degree+1);
    std::vector<double> v_right(v_degree+1);
    std::vector<double> u_bases(u_degree+1);
    std::vector<double> v_bases(v_degree+1);
    for (size_t u_s = 0; u_s < u_numSamples; u_s++) {

      double u_t = static_cast<double>(u_s)/static_cast<double>(u_numSamples);

      advance(u_intervals, u_t, u_degree, u_i, u_offset, u_left, u_right);

      compute_bases(u_intervals, u_degree, u_i, u_left, u_right, u_bases);

      size_t v_i = 0;
      double v_offset = 0.0;
      for (size_t v_s = 0; v_s < v_numSamples; v_s++) {

        double v_t = static_cast<double>(v_s)/static_cast<double>(v_numSamples);

        advance(v_intervals, v_t, v_degree, v_i, v_offset, v_left, v_right);

        compute_bases(v_intervals, v_degree, v_i, v_left, v_right, v_bases);

        uv_samples[s] = Vector::Zero();
        for (size_t u_j = 0; u_j <= u_degree; u_j++) {
          for (size_t v_j = 0; v_j <= v_degree; v_j++) {
            int u_control_idx = (int)u_i - (int)u_degree + (int)u_j;
            int v_control_idx = (int)v_i - (int)v_degree + (int)v_j;
            uv_samples[s] += u_bases[u_j] * v_bases[v_j] * uv_control[u_control_idx][v_control_idx];
          }
        }

        s++;
      }
    }
  }

  size_t u_degree;
  size_t v_degree;

  size_t u_numControl;
  size_t v_numControl;

  size_t u_numSamples;
  size_t v_numSamples;

  CVector<double> u_intervals;
  CVector<double> v_intervals;

  CVector<CVector<Vector>> uv_control;
  std::vector<Vector> uv_samples;

};

extern "C" {
  CyclicCurve* CC_construct(size_t degree, size_t numControl, size_t numSamples) {
    try {
      return new CyclicCurve(degree, numControl, numSamples);
    } catch (...)  {
      return nullptr;
    }
  }
  double * CC_get_intervals(CyclicCurve* cc) { return cc->get_intervals(); }
  double * CC_get_control(CyclicCurve* cc) { return cc->get_control(); }
  double * CC_get_samples(CyclicCurve* cc) { return cc->get_samples(); }

  CyclicSurface* CS_construct(size_t u_degree, size_t v_degree, size_t u_numControl, size_t v_numControl, size_t u_numSamples, size_t v_numSamples) {
    try {
      return new CyclicSurface(u_degree, v_degree, u_numControl, v_numControl, u_numSamples, v_numSamples);
    } catch (...)  {
      return nullptr;
    }
  }
  double * CS_get_u_intervals(CyclicSurface* cs) { return cs->get_u_intervals(); }
  double * CS_get_v_intervals(CyclicSurface* cs) { return cs->get_v_intervals(); }
  double * CS_get_n_control(CyclicSurface* cs, size_t n) { return cs->get_control(n); }
  double * CS_get_samples(CyclicSurface* cs) { return cs->get_samples(); }
}

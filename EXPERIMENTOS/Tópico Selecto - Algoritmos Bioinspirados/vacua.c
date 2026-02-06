i#include "vacua.h"

double V_lifting_optimized(double s, double tau, 
                          double AH3, double AF3, double AF5, 
                          double A3N3, double AD5) {
    // Precompute common powers
    double inv_tau3 = 1.0 / pow(tau, 3);  // 1/tau^3
    double inv_tau4 = 1.0 / pow(tau, 4);  // 1/tau^4
    double inv_tau2_5 = 1.0 / pow(tau, 2.5);  // 1/tau^(5/2)
    double inv_sqrt_s = 1.0 / sqrt(s);    // 1/sqrt(s)
    
    // Compute all terms using multiplications instead of divisions
    double term1 = AH3 * s * inv_tau3;
    double term2 = AF3 * (1.0 / s) * inv_tau3;
    double term3 = AF5 * inv_tau4;
    double term4 = A3N3 * inv_tau3;
    double term5 = AD5 * inv_sqrt_s * inv_tau2_5;
    
    return term1 + term2 + term3 + term4 + term5;
}

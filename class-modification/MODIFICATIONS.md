# NPT Modification to CLASS v3.3.4
# 
# Two files modified: source/background.c and source/input.c
#
# ============================================================
# FILE 1: source/background.c
# ============================================================
# 
# Replace the V_scf, dV_scf, ddV_scf functions (around line 2991)
# with the NPT Starobinsky potential:
#
# ORIGINAL (default CLASS quintessence):
#   V = V_e * V_p = exp(-lambda*phi) * [(phi-B)^alpha + A]
#
# REPLACEMENT (NPT completion deficit):
#   V = V_0 * (1 - exp(-alpha*phi))^2
#   where alpha = sqrt(2/3) is hardcoded
#   and V_0 = scf_parameters[0] (tuned by shooting)

# --- Cut here and replace in background.c ---

double V_scf(struct background *pba, double phi) {
  double V_0 = pba->scf_parameters[0];
  double alpha = 0.816496580927726; /* sqrt(2/3) */
  double e = exp(-alpha * phi);
  return V_0 * (1.0 - e) * (1.0 - e);
}

double dV_scf(struct background *pba, double phi) {
  double V_0 = pba->scf_parameters[0];
  double alpha = 0.816496580927726;
  double e = exp(-alpha * phi);
  return V_0 * 2.0 * alpha * e * (1.0 - e);
}

double ddV_scf(struct background *pba, double phi) {
  double V_0 = pba->scf_parameters[0];
  double alpha = 0.816496580927726;
  double e = exp(-alpha * phi);
  return V_0 * 2.0 * alpha * alpha * e * (2.0 * e - 1.0);
}

# ============================================================
# FILE 2: source/input.c  
# ============================================================
#
# In function input_get_guess(), around line 1242,
# replace the scf_tuning_index == 0 case:
#
# ORIGINAL:
#   xguess[index_guess] = sqrt(3.0/ba.Omega0_scf);
#   dxdy[index_guess] = -0.5*sqrt(3.0)*pow(ba.Omega0_scf,-1.5);
#
# REPLACEMENT:
#   xguess[index_guess] = ba.scf_parameters[ba.scf_tuning_index];
#   dxdy[index_guess] = 1.0;
#
# This allows the shooting algorithm to use the initial V_0 guess
# from scf_parameters[0] directly, rather than computing from
# the exponential potential formula which gives NaN for Omega_scf < 0.

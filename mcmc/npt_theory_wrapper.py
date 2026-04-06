"""
NPT Completion-Deficit Dark Energy: Custom Cobaya Theory Wrapper

This wrapper ensures the scf_parameters array is properly constructed
for CLASS with the NPT Starobinsky potential.

Usage in Cobaya YAML:
  theory:
    npt_theory_wrapper.NPTTheory:
      path: /path/to/class_public

Or import and use directly:
  from npt_theory_wrapper import NPTTheory
"""

import numpy as np
from cobaya.theory import Theory

class NPTTheory(Theory):
    """
    Custom Cobaya theory class for the NPT completion-deficit model.
    
    Wraps CLASS with the modified Starobinsky potential and ensures
    the scf_parameters array is correctly constructed from the
    sampled parameter N_i.
    """
    
    # Path to CLASS installation
    path: str = None
    
    def initialize(self):
        """Initialize the CLASS wrapper."""
        from classy import Class
        self.classy = Class()
        
    def get_requirements(self):
        """Parameters this theory needs from the sampler."""
        return {
            'H0': None,
            'omega_b': None, 
            'omega_cdm': None,
            'A_s': None,
            'n_s': None,
            'tau_reio': None,
            'N_i': None,
        }
    
    def calculate(self, state, want_derived=True, **params):
        """Run CLASS and store results."""
        
        N_i = self.provider.get_param('N_i')
        H0 = self.provider.get_param('H0')
        omega_b = self.provider.get_param('omega_b')
        omega_cdm = self.provider.get_param('omega_cdm')
        A_s = self.provider.get_param('A_s')
        n_s = self.provider.get_param('n_s')
        tau_reio = self.provider.get_param('tau_reio')
        
        # Construct scf_parameters: [V0_guess, unused, unused, unused, phi_ini, phi_prime_ini]
        # V0 is tuned by CLASS shooting (scf_tuning_index = 0)
        # N_i is the initial field value
        scf_params = f"1e-7,1.0,1.0,1.0,{N_i},0.0"
        
        class_params = {
            'output': 'tCl,pCl,lCl,mPk',
            'lensing': 'yes',
            'h': H0 / 100.0,
            'T_cmb': 2.7255,
            'omega_b': omega_b,
            'omega_cdm': omega_cdm,
            'N_ur': 2.0328,
            'N_ncdm': 1,
            'm_ncdm': 0.06,
            'A_s': A_s,
            'n_s': n_s,
            'tau_reio': tau_reio,
            'Omega_Lambda': 0,
            'Omega_fld': 0,
            'Omega_scf': -1,
            'scf_parameters': scf_params,
            'attractor_ic_scf': 'no',
            'scf_tuning_index': 0,
            'l_max_scalars': 2508,
            'P_k_max_h/Mpc': 1.0,
        }
        
        try:
            self.classy.set(class_params)
            self.classy.compute()
            
            # Store Cl spectra for CMB likelihoods
            state['Cl'] = self.classy.lensed_cl(2508)
            
            # Store derived parameters
            h = H0 / 100.0
            Omega_m = (omega_b + omega_cdm) / h**2
            sigma8 = self.classy.sigma8()
            
            state['derived'] = {
                'sigma8': sigma8,
                'S8': sigma8 * np.sqrt(Omega_m / 0.3),
                'age': self.classy.age(),
                'rdrag': self.classy.rs_drag(),
                'Omega_m': Omega_m,
                'theta_s_100': self.classy.theta_s_100(),
            }
            
            # Store for BAO likelihoods
            state['H'] = lambda z: self.classy.Hubble(z) * 299792.458
            state['angular_distance'] = lambda z: self.classy.angular_distance(z)
            state['rdrag'] = self.classy.rs_drag()
            
            state['success'] = True
            
        except Exception as e:
            state['success'] = False
            self.log.debug(f"CLASS failed: {e}")
            
        finally:
            try:
                self.classy.struct_cleanup()
                self.classy.empty()
            except:
                pass
    
    def get_Cl(self, ell_factor=False, units='FIRASmuK2'):
        """Return CMB Cl spectra for likelihood evaluation."""
        return self.current_state['Cl']
    
    def get_sigma8(self):
        return self.current_state['derived']['sigma8']
    
    def get_param(self, p):
        if p in self.current_state.get('derived', {}):
            return self.current_state['derived'][p]
        return None
    
    def close(self):
        try:
            self.classy.struct_cleanup()
            self.classy.empty()
        except:
            pass


# ============================================================
# ALTERNATIVE: Simple function-based approach for quick testing
# ============================================================

def npt_class_run(H0, omega_b, omega_cdm, N_i, A_s=2.1e-9, n_s=0.9649, tau_reio=0.0544):
    """
    Run CLASS with NPT potential. Returns dict of observables.
    
    Usage:
        result = npt_class_run(67.0, 0.02237, 0.115, 2.9)
        print(result['sigma8'], result['age'], result['S8'])
    """
    from classy import Class
    
    c = Class()
    c.set({
        'output': 'tCl,pCl,lCl,mPk',
        'lensing': 'yes',
        'h': H0/100, 'T_cmb': 2.7255,
        'omega_b': omega_b, 'omega_cdm': omega_cdm,
        'N_ur': 2.0328, 'N_ncdm': 1, 'm_ncdm': 0.06,
        'A_s': A_s, 'n_s': n_s, 'tau_reio': tau_reio,
        'Omega_Lambda': 0, 'Omega_fld': 0, 'Omega_scf': -1,
        'scf_parameters': f'1e-7,1,1,1,{N_i},0',
        'attractor_ic_scf': 'no', 'scf_tuning_index': 0,
        'l_max_scalars': 2508, 'P_k_max_h/Mpc': 1.0,
    })
    
    c.compute()
    
    h = H0/100
    Om = (omega_b + omega_cdm) / h**2
    sig8 = c.sigma8()
    
    result = {
        'age': c.age(),
        'sigma8': sig8,
        'S8': sig8 * np.sqrt(Om/0.3),
        'theta_s_100': c.theta_s_100(),
        'rs_drag': c.rs_drag(),
        'Omega_m': Om,
        'H0': H0,
        'N_i': N_i,
    }
    
    c.struct_cleanup()
    c.empty()
    
    return result

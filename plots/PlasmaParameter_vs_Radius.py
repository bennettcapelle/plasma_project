import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data'))
 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import astropy.units as u
from plasmapy.formulary import Debye_length
from parameters import data, DEVICES, REGIONS, TOKAMAKS, STELLARATORS

# Visual encoding
 
REGION_MARKER = {'core': 'o', 'edge': 's', 'sol': '^'}
REGION_LABEL  = {'core': 'Core', 'edge': 'Edge', 'sol': 'SOL'}
REGION_SIZE   = {'core': 120,    'edge': 100,     'sol': 90}

# Physics helpers
 
def compute_debye(Te_keV, ne_m3):
    """Electron Debye length [m] via PlasmaPy."""
    T_J = (Te_keV * u.keV).to(u.J, equivalencies=u.temperature_energy())
    return Debye_length(T_e=T_J, n_e=ne_m3 * u.m**-3).to(u.m).value
 
def compute_Lambda(Te_keV, ne_m3):
    """Plasma parameter: number of particles in a Debye sphere.
    Lambda = (4pi/3) * ne * lambda_De^3
    Cross-checked against Freidberg:
    Lambda = 5.4e6 * T_k^(3/2) / n_20^(1/2)"""
    lam = compute_debye(Te_keV, ne_m3)
    return (4 * np.pi / 3) * ne_m3 * lam**3

# Figure
 
fig, ax = plt.subplots(figsize=(8.5, 6.5))
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(0.05, 5)
ax.set_ylim(1e4, 1e11)

# Scatter: Lambda vs minor radius a
 
for device, params in data.items():
    color    = params['color']
    is_stell = params['type'] == 'stellarator'
    a        = params['a']
    for region in REGIONS:
        if region not in params:
            continue
        Lam = compute_Lambda(params[region]['Te'], params[region]['ne'])
        ax.scatter(a, Lam,
                   marker=REGION_MARKER[region],
                   s=REGION_SIZE[region],
                   facecolors='none' if is_stell else color,
                   edgecolors=color,
                   linewidths=1.6,
                   zorder=3)

# Second y-axis: nu_ee / omega_pe = 1 / (3 Lambda)  (Freidberg)
 
ax2 = ax.twinx()
ax2.set_yscale('log')
y_min, y_max = ax.get_ylim()
ax2.set_ylim(1 / (3 * y_min), 1 / (3 * y_max))
ax2.set_ylabel(r'Collisionality  $\nu_{ee}/\omega_{pe} = 1/(3\Lambda)$', fontsize=11)
ax2.tick_params(which='both', direction='in')

# Axes formatting
 
ax.set_xlabel(r'Minor radius $a$  [m]', fontsize=12)
ax.set_ylabel(r'Plasma parameter $\Lambda$', fontsize=12)
ax.set_title(r'Plasma parameter $\Lambda$ vs device size', fontsize=13, pad=10)
ax.tick_params(which='both', direction='in', top=True)
ax.grid(True, which='major', linestyle=':', linewidth=0.5, color='0.80', zorder=0)

# Legends
 
type_handles = [
    mlines.Line2D([], [], marker='o', color='0.3', markersize=8,
                  linestyle='None', markerfacecolor='0.3',
                  label='Tokamak (filled)'),
    mlines.Line2D([], [], marker='o', color='0.3', markersize=8,
                  linestyle='None', markerfacecolor='none', markeredgewidth=1.6,
                  label='Stellarator (open)'),
]
region_handles = [
    mlines.Line2D([], [], marker=REGION_MARKER[r], color='0.3', markersize=8,
                  linestyle='None', markerfacecolor='0.3',
                  label=REGION_LABEL[r])
    for r in REGIONS
]
device_handles = [
    mlines.Line2D([], [], marker='o', color=data[d]['color'], markersize=7,
                  linestyle='None', markerfacecolor=data[d]['color'],
                  label=d)
    for d in DEVICES
]
 
fig.tight_layout()
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
X_LEFT   = 0.0   # fixed left anchor for all three legends
 
leg_type = ax.legend(handles=type_handles,
                     title='Type', title_fontsize=8,
                     fontsize=8, loc='upper left',
                     bbox_to_anchor=(X_LEFT, 1.0),
                     framealpha=0.9, edgecolor='0.8')
ax.add_artist(leg_type)
 
fig.canvas.draw()
y1 = leg_type.get_window_extent(renderer).transformed(ax.transAxes.inverted()).y0
 
leg_region = ax.legend(handles=region_handles,
                       title='Region', title_fontsize=8,
                       fontsize=8, loc='upper left',
                       bbox_to_anchor=(X_LEFT, y1),
                       framealpha=0.9, edgecolor='0.8')
ax.add_artist(leg_region)
 
fig.canvas.draw()
y2 = leg_region.get_window_extent(renderer).transformed(ax.transAxes.inverted()).y0
 
ax.legend(handles=device_handles,
          title='Device', title_fontsize=8,
          fontsize=8, loc='upper left',
          bbox_to_anchor=(X_LEFT, y2),
          framealpha=0.9, edgecolor='0.8')

# Save
 
plt.savefig('plots/PlasmaParameter_vs_Radius.pdf', dpi=200, bbox_inches='tight')
plt.savefig('plots/PlasmaParameter_vs_Radius.png', dpi=200, bbox_inches='tight')
print("Saved PlasmaParameter_vs_Radius.pdf and PlasmaParameter_vs_Radius.png")

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data'))
 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import astropy.units as u
from plasmapy.formulary import Debye_length
from parameters import data, DEVICES, REGIONS, TOKAMAKS, STELLARATORS

# Visual encoding  (mirrors Temp_vs_Density.py)
 
REGION_MARKER = {'core': 'o', 'edge': 's', 'sol': '^'}
REGION_LABEL  = {'core': 'Core', 'edge': 'Edge', 'sol': 'SOL'}
REGION_SIZE   = {'core': 120,    'edge': 100,     'sol': 90}

# Physics helper
 
def compute_debye(Te_keV, ne_m3):
    """Electron Debye length [m] via PlasmaPy.
    Cross-checked against Freidberg:
    lambda_D = 2.35e-5 * sqrt(T_k / n_20)  [m]"""
    T_J = (Te_keV * u.keV).to(u.J, equivalencies=u.temperature_energy())
    return Debye_length(T_e=T_J, n_e=ne_m3 * u.m**-3).to(u.m).value

# Figure
 
fig, ax = plt.subplots(figsize=(8.5, 6.5))
ax.set_xscale('log')
ax.set_yscale('log')
 
# Limits set explicitly to avoid autoscale surprises.
# ne range: ISTTOK SOL (3.5e17) to ITER core (9.8e19)
# lam range: TCV SOL (~7e-6 m) to HSX core (~1.4e-4 m)
ax.set_xlim(1e17, 5e20)
ax.set_ylim(2e-6, 5e-4)

# Scatter: lambda_D vs ne
 
for device, params in data.items():
    color    = params['color']
    is_stell = params['type'] == 'stellarator'
    for region in REGIONS:
        if region not in params:
            continue
        lam = compute_debye(params[region]['Te'], params[region]['ne'])
        ax.scatter(params[region]['ne'], lam,
                   marker=REGION_MARKER[region],
                   s=REGION_SIZE[region],
                   facecolors='none' if is_stell else color,
                   edgecolors=color,
                   linewidths=1.6,
                   zorder=3)

# Axes formatting
 
ax.set_xlabel(r'Electron density $n_e$  [m$^{-3}$]', fontsize=12)
ax.set_ylabel(r'Electron Debye length $\lambda_{D}$  [m]', fontsize=12)
ax.set_title(r'Debye Length vs Electron Density', fontsize=13, pad=10)
ax.tick_params(which='both', direction='in', top=True, right=True)
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
 
# Type legend:
leg_type = ax.legend(handles=type_handles,
                     title='Type', title_fontsize=8,
                     fontsize=8, loc='upper right',
                     framealpha=0.9, edgecolor='0.8')
ax.add_artist(leg_type)
 
# Region legend
fig.canvas.draw()
bbox_type_ax = leg_type.get_window_extent(fig.canvas.get_renderer()).transformed(ax.transAxes.inverted())
leg_region = ax.legend(handles=region_handles,
                       title='Region', title_fontsize=8,
                       fontsize=8, loc='upper right',
                       bbox_to_anchor=(bbox_type_ax.x1, bbox_type_ax.y0),
                       framealpha=0.9, edgecolor='0.8')
ax.add_artist(leg_region)
 
# Device legend:
ax.legend(handles=device_handles,
          title='Device', title_fontsize=8,
          fontsize=8, loc='lower left',
          framealpha=0.9, edgecolor='0.8')
 
# Save
 
plt.savefig('plots/DebyeLength_vs_Density.pdf', dpi=200, bbox_inches='tight')
plt.savefig('plots/DebyeLength_vs_Density.png', dpi=200, bbox_inches='tight')
print("Saved DebyeLength_vs_Density.pdf and DebyeLength_vs_Density.png")
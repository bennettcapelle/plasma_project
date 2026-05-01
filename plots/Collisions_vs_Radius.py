import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data'))

import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import astropy.units as u
from plasmapy.formulary.collisions import Coulomb_logarithm
from plasmapy.formulary.collisions.frequencies import MaxwellianCollisionFrequencies
from parameters import data, DEVICES, REGIONS, TOKAMAKS, STELLARATORS

# Visual encoding

REGION_MARKER = {'core': 'o', 'edge': 's', 'sol': '^'}
REGION_LABEL  = {'core': 'Core', 'edge': 'Edge', 'sol': 'SOL'}
REGION_SIZE   = {'core': 120,    'edge': 100,     'sol': 90}

# Physics helper

def compute_nu_ee(Te_keV, ne_m3):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        T = (Te_keV * u.keV).to(u.J, equivalencies=u.temperature_energy())
        n = ne_m3 * u.m**-3
        lnL = Coulomb_logarithm(T, n, ('e-', 'e-'))
        return MaxwellianCollisionFrequencies(
            'e-', 'e-', v_drift=0 * u.m / u.s,
            T_a=T, n_a=n, T_b=T, n_b=n,
            Coulomb_log=lnL
        ).Lorentz_collision_frequency.to(u.Hz).value

# Collect all values first to set y-axis limits from data

all_nu = [
    compute_nu_ee(params[region]['Te'], params[region]['ne'])
    for params in data.values()
    for region in REGIONS
    if region in params
]

# Figure

fig, ax = plt.subplots(figsize=(8.5, 6.5))
ax.set_xscale('log')
ax.set_yscale('log')
# Extended x range gives breathing room on both sides of the data
ax.set_xlim(0.02, 10)
ax.set_ylim(min(all_nu) * 0.3, max(all_nu) * 5)

# Scatter: nu_ee vs minor radius a

for device, params in data.items():
    color    = params['color']
    is_stell = params['type'] == 'stellarator'
    a        = params['a']
    for region in REGIONS:
        if region not in params:
            continue
        nu = compute_nu_ee(params[region]['Te'], params[region]['ne'])
        ax.scatter(a, nu,
                   marker=REGION_MARKER[region],
                   s=REGION_SIZE[region],
                   facecolors='none' if is_stell else color,
                   edgecolors=color,
                   linewidths=1.6,
                   zorder=3)

# Axes formatting

ax.set_xlabel(r'Minor radius $a$  [m]', fontsize=12)
ax.set_ylabel(r'Electron collision frequency $\nu_{ee}$  [Hz]', fontsize=12)
ax.set_title(r'Electron collision frequency vs device size', fontsize=13, pad=10)
ax.tick_params(which='both', direction='in', top=True, right=True)
ax.grid(True, which='major', linestyle=':', linewidth=0.5, color='0.80', zorder=0)

# Legends — stacked on the left with flush left edges

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
X_LEFT   = 0.0

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

plt.savefig('plots/collision_frequency.pdf', dpi=200, bbox_inches='tight')
plt.savefig('plots/collision_frequency.png', dpi=200, bbox_inches='tight')
print("Saved collision_frequency.pdf and collision_frequency.png")
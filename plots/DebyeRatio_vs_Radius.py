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

# Physics helper

def compute_debye(Te_keV, ne_m3):
    """
    Electron Debye length [m] via PlasmaPy.
    Cross-checked against Freidberg:
        lambda_De = 2.35e-5 * sqrt(T_k / n_20)  [m]
    """
    T_J = (Te_keV * u.keV).to(u.J, equivalencies=u.temperature_energy())
    return Debye_length(T_e=T_J, n_e=ne_m3 * u.m**-3).to(u.m).value

# Figure

fig, ax = plt.subplots(figsize=(8.5, 6.5))
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(0.02, 10)
ax.set_ylim(1e-6, 1e1)

# Reference regions

ax.axhline(1.0, color='0.4', linewidth=1.1, linestyle='--', zorder=2)

# Scatter: lambda_De/a vs minor radius a

for device, params in data.items():
    color    = params['color']
    is_stell = params['type'] == 'stellarator'
    a        = params['a']
    for region in REGIONS:
        if region not in params:
            continue
        lam   = compute_debye(params[region]['Te'], params[region]['ne'])
        ratio = lam / a
        ax.scatter(a, ratio,
                   marker=REGION_MARKER[region],
                   s=REGION_SIZE[region],
                   facecolors='none' if is_stell else color,
                   edgecolors=color,
                   linewidths=1.6,
                   zorder=3)

# Axes formatting

ax.set_xlabel(r'Minor radius $a$  [m]', fontsize=12)
ax.set_ylabel(r'$\lambda_{De} / a$', fontsize=13)
ax.set_title(r'Plasma criterion $\lambda_{De} \ll a$ across devices and regions',
             fontsize=13, pad=10)
ax.tick_params(which='both', direction='in', top=True, right=True)
ax.grid(True, which='major', linestyle=':', linewidth=0.5, color='0.80', zorder=1)

# Legends — stacked flush left, same pattern as other figures

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

plt.savefig('plots/DebyeRatio_vs_Radius.pdf', dpi=200, bbox_inches='tight')
plt.savefig('plots/DebyeRatio_vs_Radius.png', dpi=200, bbox_inches='tight')
print("Saved lDebyeRatio_vs_Radius.pdf and DebyeRatio_vs_Radius.png")
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data'))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from parameters import data, DEVICES, REGIONS, TOKAMAKS, STELLARATORS

# Visuals

REGION_MARKER = {'core': 'o', 'edge': 's', 'sol': '^'}
REGION_LABEL  = {'core': 'Core', 'edge': 'Edge', 'sol': 'SOL'}
REGION_SIZE   = {'core': 120,    'edge': 100,     'sol': 90}

DEBYE_CONTOURS = [1e-6, 1e-5, 1e-4, 1e-3]
DEBYE_LABELS   = [r'$\lambda_{D} = 1\,\mu$m',
                  r'$\lambda_{D} = 10\,\mu$m',
                  r'$\lambda_{D} = 0.1\,$mm',
                  r'$\lambda_{D} = 1\,$mm']
DEBYE_COLOR = '0.60'

# Physics helpers

def Te_for_constant_debye(lam_De, ne_array):
    return (lam_De / 2.35e-5) ** 2 * (ne_array / 1e20)

# Figure setup

fig, ax = plt.subplots(figsize=(8.5, 6.5))
ax.set_xscale('log')
ax.set_yscale('log')

X_MIN, X_MAX = 1e16, 5e21
Y_MIN, Y_MAX = 3e-3, 5e1
ax.set_xlim(X_MIN, X_MAX)
ax.set_ylim(Y_MIN, Y_MAX)

# Debye length contour lines

ne_range = np.logspace(np.log10(X_MIN), np.log10(X_MAX), 500)
for lam in DEBYE_CONTOURS:
    ax.plot(ne_range, Te_for_constant_debye(lam, ne_range),
            color=DEBYE_COLOR, linewidth=0.9, linestyle='--', zorder=1)

# Scatter points

for device, params in data.items():
    color    = params['color']
    is_stell = params['type'] == 'stellarator'
    for region in REGIONS:
        if region not in params:
            continue
        ax.scatter(params[region]['ne'], params[region]['Te'],
                   marker=REGION_MARKER[region],
                   s=REGION_SIZE[region],
                   facecolors='none' if is_stell else color,
                   edgecolors=color,
                   linewidths=1.6,
                   zorder=3)

ax.set_xlabel(r'Electron density $n_e$  [m$^{-3}$]', fontsize=12)
ax.set_ylabel(r'Electron temperature $T_e$  [keV]',  fontsize=12)
ax.set_title(r'Electron Temperature vs Density',
             fontsize=13, pad=10)
ax.tick_params(which='both', direction='in', top=True, right=True)
ax.grid(True, which='major', linestyle=':', linewidth=0.5, color='0.80', zorder=0)

fig.tight_layout()
fig.canvas.draw()

# Debye length labels

_p1 = ax.transData.transform((1e18, Te_for_constant_debye(1e-5, 1e18)))
_p2 = ax.transData.transform((1e19, Te_for_constant_debye(1e-5, 1e19)))
line_angle = np.degrees(np.arctan2(_p2[1] - _p1[1], _p2[0] - _p1[0]))

log_frac = 0.93   # adjust to slide all labels along their lines simultaneously

for lam, label in zip(DEBYE_CONTOURS, DEBYE_LABELS):
    ne_min_vis = max(X_MIN, Y_MIN * 1e20 / (lam / 2.35e-5) ** 2)
    ne_max_vis = min(X_MAX, Y_MAX * 1e20 / (lam / 2.35e-5) ** 2)

    ne_label = 10 ** (np.log10(ne_min_vis) + log_frac * (np.log10(ne_max_vis) - np.log10(ne_min_vis)))
    Te_label = Te_for_constant_debye(lam, ne_label)

    ax.text(ne_label, Te_label, label,
            fontsize=7.5, color=DEBYE_COLOR,
            ha='right', va='bottom',
            rotation=line_angle,
            rotation_mode='anchor')

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
debye_handle = mlines.Line2D([], [], color=DEBYE_COLOR, linestyle='--',
                              linewidth=1.0, label=r'$\lambda_{De}$ = const')

# Type legend: top left
leg_type = ax.legend(handles=type_handles,
                     title='Type', title_fontsize=8,
                     fontsize=8, loc='upper left',
                     framealpha=0.9, edgecolor='0.8')
ax.add_artist(leg_type)

# Measure type legend so region legend butts up directly below it
fig.canvas.draw()
bbox_type_ax = leg_type.get_window_extent(fig.canvas.get_renderer()).transformed(ax.transAxes.inverted())

leg_region = ax.legend(handles=region_handles,
                       title='Region', title_fontsize=8,
                       fontsize=8, loc='upper left',
                       bbox_to_anchor=(bbox_type_ax.x0, bbox_type_ax.y0),
                       framealpha=0.9, edgecolor='0.8')
ax.add_artist(leg_region)

# Device + Debye line: bottom right
ax.legend(handles=device_handles + [debye_handle],
          title='Device', title_fontsize=8,
          fontsize=8, loc='lower right',
          framealpha=0.9, edgecolor='0.8')

# Save

plt.savefig('plots/Temp_vs_Density.pdf', dpi=200, bbox_inches='tight')
plt.savefig('plots/Temp_vs_Density.png', dpi=200, bbox_inches='tight')
print("Saved Temp_vs_Density.pdf and Temp_vs_Density.png")
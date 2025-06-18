import os

import numpy as np
import pandas as pd
import click
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap
import matplotlib.patches as patches

from data.table_coordinates import get_special_coordinates, get_classic_coordinates


def make_table_fig():
    """Create a base periodic table figure with empty boxes and element
    symbols.

    Returns:
        tuple[plt.Figure, plt.Axes]: The matplotlib figure and axes objects.
    """
    special_coords = get_special_coordinates()
    coords = get_classic_coordinates()
    x_vals = [x for x, _ in coords.values()]
    y_vals = [y for _, y in coords.values()]

    x_min, x_max = min(x_vals), max(x_vals)
    y_min, y_max = min(y_vals), max(y_vals)

    fig, ax = plt.subplots(figsize=(x_max - x_min + 2, y_max - y_min + 2))

    for symbol, (x, y) in coords.items():
        rect = patches.Rectangle(
            (x - 0.5, y - 0.5), 1, 1, edgecolor="black", linewidth=1.3, facecolor="none"
        )
        ax.add_patch(rect)

    for label, (x, y) in special_coords.items():
        ax.text(x, y, label, ha="center", va="center", fontsize=22)

    ax.set_xlim(x_min - 1, x_max + 1)
    ax.set_ylim(y_min - 1, y_max + 1)
    ax.set_aspect("equal")
    ax.axis("off")

    return fig, ax


def color_elements(ax, values: dict[str, float]):
    """Color elements on a periodic table plot and display a horizontal
    colorbar."""
    coords = get_classic_coordinates()
    cmap_name = "GnBu"
    cmap = get_cmap(cmap_name)

    vmin = min(values.values())
    vmax = max(values.values())
    norm = Normalize(vmin=vmin, vmax=vmax)

    # color each element
    for symbol, val in values.items():
        if symbol not in coords:
            continue
        x, y = coords[symbol]
        if val == 0:
            # no color for zero counts
            rect = patches.Rectangle(
                (x - 0.5, y - 0.5), 1, 1, facecolor="none", edgecolor="none", zorder=0
            )
            ax.add_patch(rect)
            ax.text(
                x,
                y,
                symbol,
                ha="center",
                va="center",
                fontsize=25,
                color="k",
                alpha=0.5,
            )
            continue

        rgba = cmap(norm(val))
        rect = patches.Rectangle(
            (x - 0.5, y - 0.5), 1, 1, facecolor=rgba, edgecolor="none", zorder=0
        )
        ax.add_patch(rect)

        # determine text color
        txt_color = "w" if norm(val) > 0.74 else "k"
        ax.text(
            x,
            y,
            symbol,
            ha="center",
            va="center",
            fontsize=25,
            color=txt_color,
            alpha=1.0,
        )

    # add colorbar with 6 integer ticks
    ticks = sorted(set([int(i) for i in np.linspace(vmin, vmax, 6)]))
    dummy = np.linspace(vmin, vmax, 100).reshape(1, -1)
    im = ax.imshow(dummy, extent=[0, 1, 0, 0.1], cmap=cmap_name, visible=False)
    cax = ax.inset_axes((0.19, 0.77, 0.4, 0.02))
    cbar = plt.colorbar(im, cax=cax, orientation="horizontal", ticks=ticks)
    cbar.ax.tick_params(labelsize=22)
    cbar.set_label("Element Count", fontsize=25, loc="center")


def element_prevalence(
    elem_tracker,
    excel_file_path,
    script_path,
    log_scale=False,
    ptable_fig=True,
):

    if ptable_fig:
        fig, ax = make_table_fig()

        values = {}
        skip = {
            "Fr",
            "Ra",
            "Rf",
            "Db",
            "Sg",
            "Bh",
            "Hs",
            "Mt",
            "Ds",
            "Rg",
            "Cn",
            "Nh",
            "Fl",
            "Mc",
            "Lv",
            "Ts",
            "Og",
        }
        for symbol, count in elem_tracker.items():
            if symbol in skip:
                continue
            if log_scale:
                count = np.log(count) if count > 0 else 0
            values[symbol] = count

        color_elements(ax, values)

        # remove extension from filename
        base = os.path.basename(os.path.normpath(excel_file_path))
        name, _ = os.path.splitext(base)
        file_name = (
            f"{name}_ptable.png" if not name.endswith("_ptable") else f"{name}.png"
        )
        fig_name = os.path.join(script_path, file_name)
        plt.savefig(fig_name, format="png", bbox_inches="tight", dpi=500)
        click.secho(f"Periodic table created successfully in {fig_name}", fg="cyan")
        plt.draw()

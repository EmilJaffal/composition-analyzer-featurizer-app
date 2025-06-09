import os

import click
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
from matplotlib.colors import Normalize


def element_prevalence(
    elem_tracker,
    excel_file_path,
    script_path,
    log_scale=False,
    ptable_fig=True,
):
    ptable_path = os.path.join(script_path, "ptable.csv")

    ptable = pd.read_csv(ptable_path)
    ptable.index = ptable["symbol"].values

    n_row = ptable["row"].max()
    n_column = ptable["column"].max()

    if ptable_fig:
        fig, ax = plt.subplots(
            figsize=(n_column + 2, n_row + 2)
        )  # Adjusted figure size
        rows = ptable["row"]
        columns = ptable["column"]
        symbols = ptable["symbol"]
        rw = 1.0  # rectangle width (rw)
        rh = 1.0  # rectangle height (rh)

        # Define a 7-color scale: 0 is white, then 5 blues, last is navy
        scale_colors = [
            "#ffffff",  # white for zero
            "#ffffe0",  # pale yellow
            "#b3d8ff",  # light blue
            "#40e0d0",  # teal
            "#1e90ff",  # dodger blue
            "#005bb5",  # medium blue
            "#001f3f",  # navy (very dark blue)
        ]

        # Calculate min and max counts for binning
        counts = np.array(elem_tracker.values)
        count_max = counts.max()

        # Compute bin edges for 7 bins: 0, step1, ..., step5, max
        bin_edges = np.linspace(0, count_max, 7)
        bin_edges = np.round(bin_edges).astype(int)
        bin_edges[-1] = count_max  # Ensure last edge is exactly max

        # For np.digitize, use all but the last edge
        digitize_edges = bin_edges[:-1]  # [0, step1, ..., step5]

        for row, column, symbol in zip(rows, columns, symbols):
            row = ptable["row"].max() - row
            if symbol in [
                "Fr", "Ra", "Rf", "Db", "Sg", "Bh", "Hs", "Mt",
                "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og",
            ]:
                continue

            count = elem_tracker[symbol]
            if log_scale:
                count = np.log(count) if count != 0 else 0

            # Special case: assign max value to the last bin
            if count == count_max:
                bin_idx = 6
            else:
                bin_idx = np.digitize(count, digitize_edges, right=False) - 1
                bin_idx = min(max(bin_idx, 0), 6)
            color = scale_colors[bin_idx]

            rect = patches.Rectangle(
                (column, row),
                rw,
                rh,
                linewidth=2,
                edgecolor="black",
                facecolor=color,
                alpha=1,
            )

            plt.text(
                column + rw / 2,
                row + rw / 2,
                symbol,
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=20,
                fontweight="semibold",
                color="black",
            )
            ax.add_patch(rect)

        # Draw gradient scale on top of the periodic table
        scale_height = 1.1
        scale_width = n_column * 0.6
        scale_x = (n_column - scale_width) / 2.5
        scale_y = n_row + 0.3
        granularity = 7  # 7 rectangles

        for i in range(granularity):
            if i == 0:
                value = 0
            elif i == granularity - 1:
                value = count_max
            else:
                value = int(bin_edges[i])
            color = scale_colors[i]

            x_loc = scale_x + scale_width / granularity * i
            width = scale_width / granularity
            height = scale_height
            rect = patches.Rectangle(
                (x_loc, scale_y),
                width,
                height,
                linewidth=2,
                edgecolor="gray",
                facecolor=color,
                alpha=1,
            )
            ax.add_patch(rect)

            plt.text(
                x_loc + width / 2,
                scale_y - 0.3,
                str(value),
                horizontalalignment="center",
                verticalalignment="top",
                fontsize=16,
                fontweight="semibold",
                color="black",
            )

        # Add "Element Count" label (move outside the loop)
        plt.text(
            scale_x + scale_width / 2,
            scale_y + 2.0,
            "Element Count",
            horizontalalignment="center",
            verticalalignment="bottom",
            fontsize=16,
            fontweight="semibold",
            color="black",
        )

        # Set plot limits and turn off axis
        ax.set_ylim(-1.5, n_row + 3)
        ax.set_xlim(-0.75, n_column + 2.5)
        ax.axis("off")

        # Save the figure
        base_name = os.path.basename(os.path.normpath(excel_file_path))
        file_name = (
            f"{base_name}_ptable.png"
            if not base_name.endswith("_ptable")
            else f"{base_name}.png"
        )
        fig_name = os.path.join(script_path, file_name)
        plt.savefig(fig_name, format="png", bbox_inches="tight", dpi=600)
        click.secho(f"Periodic table created successfully in {fig_name}", fg="cyan")

        plt.draw()
        # plt.pause(0.001)
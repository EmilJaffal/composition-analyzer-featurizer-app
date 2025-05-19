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

        for row, column, symbol in zip(rows, columns, symbols):
            row = ptable["row"].max() - row
            # Condition to skip elements based on symbol
            if symbol in [
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
            ]:
                continue

            cmap = cm.GnBu  # Color
            count_min = elem_tracker.min()
            count_max = elem_tracker.max()
            count_max = count_max + 24

            norm = Normalize(vmin=count_min, vmax=count_max)
            count = elem_tracker[symbol]

            if log_scale:
                norm = Normalize(vmin=np.log(1), vmax=np.log(count_max))
                if count != 0:
                    count = np.log(count)
            color = cmap(norm(count))
            if count == 0:
                color = "white"
            if 0 < count <= 10:
                color = "lightyellow"
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
        scale_width = n_column * 0.6  # Adjusted scale width

        scale_x = (n_column - scale_width) / 2.5  # Centered horizontally
        scale_y = n_row + 0.3  # Adjusted scale position
        cmap = cm.GnBu  # Color
        granularity = 7  # Reduced granularity
        for i in range(granularity):
            value = int(round((i) * count_max / (granularity - 1)))
            if log_scale:
                if value != 0:
                    value = np.log(value)
            color = cmap(norm(value))
            if value == 0:
                color = "white"  # white
            if 0 < value <= 40:
                color = "lightyellow"
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

            # Add whole integers below the scale
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

            # Add "Element Count" label
            plt.text(
                scale_x + scale_width / 2,
                scale_y + 2.0,  # Adjust vertical position
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
        plt.close()

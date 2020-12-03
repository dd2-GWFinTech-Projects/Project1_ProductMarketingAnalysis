import pandas as pd
import plotly as px
import hvplot.pandas
import matplotlib.pyplot as plt
import panel as pn
import plotly.express as px

# pn.extension()

class PlotBuildingToools:

    def __init__(self,
        debug_level
        ):
        self.debug_level = debug_level
    
    def generate_plot__px_bar(self,
        data, x, y, color,                  # Data
        title, xlabel=None, ylabel=None,    # Labels
        barmode=None, width=None, height=None, rot=None    # Display options
        ):

        # Defaults
        if barmode is None:
            barmode="stack"

        # Build plot
        plt_ = px.bar(
            data, x=x, y=y, color=color,
            title=title,
            barmode=barmode
            )
        
        # Optional parameters
        if xlabel is not None:
            plt_.update_xaxes(title_text=xlabel)
        if ylabel is not None:
            plt_.update_yaxes(title_text=ylabel)

        if width is not None:
            plt_.update_layout(width=width)
        if height is not None:
            plt_.update_layout(height=height)
        if rot is not None:
            plt_.update_xaxes(tickangle=rot)

        # plt_.update_layout(
        #     margin=dict(l=20, r=20, t=20, b=20),
        #     paper_bgcolor="LightSteelBlue",
        # )

        return plt_

    def generate_plot__hvplot_bar(self,
        data,                  # Data
        title, xlabel, ylabel,    # Labels
        stacked=False, rot=0, width=None, height=None    # Display options
        ):

        # Defaults


        # Build plot
        if (width is not None) and (height is not None):
            plt_ = data.hvplot.bar(
                title=title, xlabel=xlabel, ylabel=ylabel,
                stacked=stacked, width=width, height=height, rot=rot
                )
        else:
            plt_ = data.hvplot.bar(
                title=title, xlabel=xlabel, ylabel=ylabel,
                stacked=stacked, rot=rot
                )

        return plt_

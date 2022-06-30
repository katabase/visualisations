from statistics import median, mean, quantiles
from plotly.colors import make_colorscale
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import json
import re

from databuilding import prep_data


# TEMPLATE TO NAME THE HTML FIGURES (! VERY IMPORTANT TO BUILD URLS AND DISPLAY THEM !)
# fig_(IDX|CAT_XXXX)(_[0-9])?
#  ^    ^     ^        ^
#  |    |     |        |_____ for the index: the identifier of the figure (7 figs are created)
#  |    |_____|______________ for the index figures: IDX ; for the catalogue figures: the cat's ID (CAT_0001...)
#  |_________________________ indicate it is a figure


def build(config, datelist, data):
    """
    average sales per catalogue and per year in 1900 francs
    :return:
    """
    # ================ NORMALIZE INPUT AND DEFINE VARIABLES ================ #
    # define color code
    colors = {"cream": "#fcf8f7", "blue": "#0000ef", "burgundy1": "#890c0c", "burgundy2": "#a41a6a", "pink": "#ff94c9"}
    scale = make_colorscale([colors["blue"], colors["burgundy2"]])  # create a colorscale
    # defining our x and y axis
    x = datelist
    y = []  # y axis of the plot: a
    # if we're in quartile mode, we have 3 y axis: q1, med, average
    if config["mode"] == "quart":
        y_q1 = []
        y_med = []
        y_q3 = []
    # if we're counting number of catalogues, we have 2 Y axis
    elif config["mode"] == "count":
        y_auc = []  # number of auction price items
        y_fix = []  # number of fixed price items
    else:
        y = []  # else, we only have 1 y axis

    # if we're counting the number of fixed price/auction items per year,
    # data is a list of the 2 dicts needed => the 1st dict is the
    # counter of fixed price items, the second of auction price items
    if type(data) == list:
        data_auc = data[1]  # dictionary mapping year - number of auction items
        data = data[0]  # dictionary mapping year - number of fixed price items
    else:
        data_auc = {}  # dummy dict for convenience (see below)

    # ================ BUILD THE Y AXIS ================ #
    for d in x:
        # if we have info for that year, build data for y
        if str(d) in list(data.keys()) or str(d) in list(data_auc.keys()):
            # average price par cat/item
            if config["mode"] == "avg":
                y.append(mean(data[str(d)]))
            # median price par cat/item
            elif config["mode"] == "med":
                y.append(median(data[str(d)]))
            # sum of price of items per year
            elif config["mode"] == "total":
                y.append(sum(data[str(d)]))
            # number of fixed/auction price items per year. we add try...except to avoid keyerrors
            elif config["mode"] == "count":
                try:
                    y_fix.append(data[str(d)])
                except KeyError:
                    pass
                try:
                    y_auc.append(data_auc[str(d)])
                except KeyError:
                    pass
            # price quarties per 5 years
            else:
                y_q1.append(data[str(d)][0])
                y_q3.append(data[str(d)][2])
                y_med.append(data[str(d)][1])
        # if we don't have info for that year, add 0 to y
        else:
            if config["mode"] == "count":
                y_fix.append(0)
                y_auc.append(0)
            elif config["mode"] == "quart":
                y_q1.append(0)
                y_med.append(0)
                y_q3.append(0)
            else:
                y.append(0)

    # ================ CREATE PLOTS ================ #
    layout, marker, hovertemplate, f_id = style(config, colors, scale)  # build style

    # clean the data provided by layout:
    # set the data on which to base the gradient: plot colors change depending on the value of y
    if config["mode"] != "count" and config["mode"] != "quart":
        marker["color"] = y
    # if config["mode"] == "count", marker and hovertemplate are lists and need to be split
    if config["mode"] == "count":
        marker0 = marker[0]
        marker1 = marker[1]
        hovertemplate0 = hovertemplate[0]
        hovertemplate1 = hovertemplate[1]
        layout["yaxis_range"] = [0, max(y_auc)]  # set maximum value

    # build figures; count and quart demand special behaviour
    if config["mode"] == "count":
        fig = go.Figure(
            data=[
                go.Bar(x=x, y=y_fix, marker=marker0, hovertemplate=hovertemplate0),
                go.Bar(x=x, y=y_auc, marker=marker1, hovertemplate=hovertemplate1)
            ],
            layout=go.Layout(layout)
        )
    elif config["mode"] == "quart":
        fig = go.Figure(
            data=[go.Box(x=x, q1=y_q1, median=y_med, q3=y_q3,
                         marker=marker,
                         fillcolor=colors["cream"],
                         width=4)
                  ],
            layout=go.Layout(layout)
        )
    else:
        fig = go.Figure(
            data=[go.Bar(x=x, y=y, marker=marker, hovertemplate=hovertemplate)],
            layout=go.Layout(layout)
        )

    # save figures
    fig.write_image(f"out/{f_id}.png")
    # with open(f"out/{f_id}", mode="w") as out:
    # fig.write()

    return None


def style(config, colors, scale):
    """
    define "non-data" elements of a figure: layout, marker, hovertemplate
    :param config: a configuration dictionary for the figure to create (see figmaker())
    :return:
            - layout a dict containing the layout for the figure
            - marker, a dict (or list if config["mode"] == "count") managing colors
            - hovertemplate, a string (or list if config["mode"] == "count") for... hover templates
            - f_id, a file identifier to build the filename (type str)
    """
    # basic layout
    layout = {
        "paper_bgcolor": colors["cream"],
        "plot_bgcolor": colors["cream"],
        "margin": {"l": 5, "r": 5, "t": 30, "b": 30},
        "showlegend": False,
        "xaxis": {"anchor": "x", "title": {"text": "Year"}},
        "barmode": "overlay"  # only affects plot 6
    }

    # defining layout, marker and hovertemplate
    if config["mode"] == "total":
        layout["yaxis"] = {"anchor": "x", "title": {"text": "Total sales"}}
        layout["title"] = "Total sales per year (in 1900 french francs)"
        layout["yaxis_range"] = [0, 75000]  # cut off the excess values
        layout["xaxis_range"] = [1844, 1955]
        marker = {"color": "", "colorscale": scale,
                  "cauto": False, "cmin": 0.00, "cmax": 65000.00}
        hovertemplate = "<b>Year</b>: %{x}<br><b>Sum of all catalogues' prices </b>: %{y:.2f} FRF<extra></extra>"

    elif config["mode"] == "avg":
        if config["level"] == "cat":
            layout["yaxis"] = {"anchor": "x", "title": {"text": "Average sales per catalogue"}}
            layout["title"] = "Average sales per catalogue and per year (in 1900 french francs)"
            layout["yaxis_range"] = [0, 10000]  # cut off the excess values
            layout["xaxis_range"] = [1844, 1955]
            marker = {"color": "", "colorscale": scale,
                      "cauto": False, "cmin": 0.00, "cmax": 7000}
            hovertemplate = "<b>Year</b>: %{x}<br><b>Average sum of prices per catalogue"\
                            + "</b>: %{y:.2f} FRF<extra></extra>"

        else:
            layout["yaxis"] = {"anchor": "x", "title": {"text": "Average item price"}}
            layout["title"] = "Average price of an item per year (in 1900 french francs)"
            layout["yaxis_range"] = [0, 32]  # cut off the excess values
            layout["xaxis_range"] = [1844, 1955]
            marker = {"color": "", "colorscale": scale,
                      "cauto": False, "cmin": 0.00, "cmax": 25}
            hovertemplate = "<b>Year</b>: %{x}<br><b>Average item price</b>: %{y:.2f} FRF<extra></extra>"

    elif config["mode"] == "med":
        if config["level"] == "cat":
            layout["yaxis"] = {"anchor": "x", "title": {"text": "Median sales per catalogue"}}
            layout["title"] = "Median price per catalogue per year (in 1900 french francs)"
            layout["yaxis_range"] = [0, 10000]  # cut off the excess values
            layout["xaxis_range"] = [1844, 1955]
            marker = {"color": "", "colorscale": scale,
                      "cauto": False, "cmin": 0.00, "cmax": 8000}
            hovertemplate = "<b>Year</b>: %{x}<br><b>Median sales per catalogue"\
                            + "</b>: %{y:.2f} FRF<extra></extra>"

        else:
            layout["yaxis"] = {"anchor": "x", "title": {"text": "Median item price"}}
            layout["title"] = "Median price of an item per year (in 1900 french francs)"
            layout["yaxis_range"] = [0, 32]  # cut off the excess values
            marker = {"color": "", "colorscale": scale,
                      "cauto": False, "cmin": 0.00, "cmax": 25}
            hovertemplate = "<b>Year</b>: %{x}<br><b>Median item price</b>: %{y:.2f} FRF<extra></extra>"

    elif config["mode"] == "count":  # fixed items first, auction after
        layout["yaxis"] = {"anchor": "x", "title": {"text": "Number of items for sale"}}
        layout["title"] = "Number of items for sale per year"
        layout["xaxis_range"] = [1840, 1955]
        marker = [{"color": colors["burgundy2"], "opacity": 0.7},
                  {"color": colors["blue"], "opacity": 0.55}]
        hovertemplate = ["<b>Year</b>: %{x}<br><b>Number of fixed-price items for sale </b>: %{y}<extra></extra>",
                         "<b>Year</b>: %{x}<br><b>Number of auction items for sale </b>: %{y}<extra></extra>"]

    else:
        layout["yaxis"] = {"anchor": "x", "title": {"text": "Price of an item (in quartiles)"}}
        layout["title"] = "Evolution of the price of an item (in 5 year ranges, in quartiles and in 1900 francs)"
        layout["yaxis_range"] = [0, 80]  # cut off the excess values
        layout["xaxis_range"] = [1840, 1925]
        marker = {"color": colors["blue"]}
        hovertemplate = ""  # no hovertemplate

    # build the file identifier
    f_id = f"fig_{config['mode']}_{config['level']}"

    return layout, marker, hovertemplate, f_id


def figmaker():
    """
    create all figures
    :return:
    """
    # defining our variables
    datelist, pdict_ls_cat, pdict_ls_item, cdict_auc_item, cdict_fix_item, quart_ls_item = prep_data()
    datelist = list(range(int(datelist[0]) - 1, int(datelist[-1]) + 1))  # years between the extremes of datelist (included)

    # making the figures
    print(0)
    build({"mode": "total", "level": "cat"}, datelist, pdict_ls_cat)
    print(1)
    build({"mode": "avg", "level": "cat"}, datelist, pdict_ls_cat)
    print(2)
    build({"mode": "med", "level": "cat"}, datelist, pdict_ls_cat)
    print(3)
    build({"mode": "avg", "level": "itm"}, datelist, pdict_ls_item)
    print(4)
    build({"mode": "med", "level": "itm"}, datelist, pdict_ls_item)
    print(5)
    build({"mode": "count", "level": "itm"}, datelist, [cdict_fix_item, cdict_auc_item])
    print(6)
    build({"mode": "quart", "level": "itm"}, datelist, quart_ls_item)

    return None


if __name__ == "__main__":
    figmaker()

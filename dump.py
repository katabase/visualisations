# --------------------
# dump of unused stuff
# --------------------


def total(datelist, colors, scale, layout):
    """
    total sales per year in year 1900 francs
    :return:
    """
    # y_total = []  # y axis of the plot: total of the sales in a year
    # x = list(range(int(datelist[0]) - 1, int(datelist[-1]) + 1))  # years between the extremes of datelist (included)
    # for d in x:
    #     if str(d) in list(pdict_ls_cat.keys()):
    #         y_total.append(sum(pdict_ls_cat[str(d)]))
    #     else:
    #        y_total.append(0)


def cat_med(datelist, colors, scale, layout):
    """
    median sales per catalogue and per year in 1900 francs
    :return:
    """
    x = list(range(int(datelist[0]) - 1, int(datelist[-1]) + 1))  # years between the extremes of datelist (included)
    y_med_cat = []  # y axis of the plot: median catalogue sales in a year
    for d in x:
        if str(d) in list(pdict_ls_cat.keys()):
            y_med_cat.append(median(pdict_ls_cat[str(d)]))
        else:
            y_med_cat.append(0)



def itm_avg(datelist, colors, scale, layout):
    """
    average price of an item per year in 1900 francs
    :return:
    """
    x = list(range(int(datelist[0]) - 1, int(datelist[-1]) + 1))  # years between the extremes of datelist (included)
    for d in x:
        if str(d) in list(pdict_ls_cat.keys()):
            y_avg_cat.append(mean(pdict_ls_cat[str(d)]))
            y_med_cat.append(median(pdict_ls_cat[str(d)]))
        else:
            y_avg_cat.append(0)
            y_med_cat.append(0)
        if str(d) in list(pdict_ls_item.keys()):
            y_avg_item.append(mean(pdict_ls_item[str(d)]))
            y_med_item.append(median(pdict_ls_item[str(d)]))
        else:
            y_avg_item.append(0)
            y_med_item.append(0)






def itm_med(datelist, colors, scale, layout):
    """
    median price of an item per year in 1900 francs
    :return:
    """
    x = list(range(int(datelist[0]) - 1, int(datelist[-1]) + 1))  # years between the extremes of datelist (included)

def itm_quartiles(datelist, colors, scale, layout):
    """
    box charts with quartiles of item prices for every 5 years
    :return:
    """
    x = list(range(int(datelist[0]) - 1, int(datelist[-1]) + 1))  # years between the extremes of datelist (included)


def itm_count(datelist, colors, scale, layout):
    """
    number of fixed and auction price items on sale per year
    :return:
    """
    x = list(range(int(datelist[0]) - 1, int(datelist[-1]) + 1))  # years between the extremes of datelist (included)






def figmaker_idx(datelist, colors, scale, layout):
    """
    create the figures to be displayed on the index page. 7 figures are created:
    - total sales per year (bar graph)
    - average sales for a whole catalogue per year (bar graph)
    - median sales for a whole catalogue per year (bar graph)
    - average sale price of an item per year (bar graph)
    - median sale price of an item per year (bar graph)
    - number of items per sale for year (2 overlayed bar graphs)

    the basis of plotly is to map data on an x and y axis ; both x and y are arrays.
    so what is needed is to create data for an x and y axis, so that the y data can
    be properly mapped to x (the y data for year 1234 must be at the same position
    as the year 1234 on the x axis. hope that makes sense).

    the figures are created in 3 steps:
    - the data is created by looping through the 2 json files and storing relevant
      data in dictionaries. those dictionaries take a year as key and other data as
      value. after that, the dictionaries are sorted and prepared to build the y axis
    - the x and y axis are created.
      - x = array containing every year between the two extreme dates for which there is price info
      - y = the relevant data (prices, number of items...) ; if there is no data, for a year,
        the value of 0 is added
    - the figures are created ; they are saved in APP/templates/partials as html files

    the figures are called within the html page using a URL : this url points to a flask route
    that renders the html files. the urls for this flask route are built using url_for
    (for the figure displayed by default) or javascript. the figures are displayed within an
    iframe.

    :return: figpath (boolean; True if figures are created; False if not)
    """
    # ============== DEFINING VARIABLES ============== #
    x = []  # x axis of the plot : years
    y_avg_cat = []  # y axis of the plot: average sales per catalog in a year
    y_med_cat = []  # y axis of the plot: median catalogue sales in a year
    y_avg_item = []  # y axis of the plot: average item price per year
    y_med_item = []  # y axis of the plot: median item price per year
    y_fix_item = []  # y axis of the plot: sum of fixed price items per year
    y_auc_item = []  # y axis of the plot: sum of non-fixed price items per year
    y_q1_gpitem = []  # y axis of the plot: the first quartile of item prices per 5 year range
    y_med_gpitem = []  # y axis of the plot: the median of item prices per 5 year range
    y_q3_gpitem = []  # y axis of the plot: the third quartile of item prices per 5 year range


    # ============== BUILD THE X AND Y AXIS ============== #
    x = list(range(int(datelist[0] ) -1, int(datelist[-1] ) +1))  # years between the extremes of datelist (included)
    # loop through all the dates; if the date is a key in the dictionnaries, it means that there
    # data associated with that year. in that case, in that case, add the data for that year to the y axis; else, add
    # 0 to y_total and y_avg_cat. in turn, the y axis are populated with data if it exists, with 0 it doesn't
    for d in x:
        if str(d) in list(pdict_ls_cat.keys()):
            y_avg_cat.append(mean(pdict_ls_cat[str(d)]))
            y_med_cat.append(median(pdict_ls_cat[str(d)]))
        else:
            y_avg_cat.append(0)
            y_med_cat.append(0)
        if str(d) in list(pdict_ls_item.keys()):
            y_avg_item.append(mean(pdict_ls_item[str(d)]))
            y_med_item.append(median(pdict_ls_item[str(d)]))
        else:
            y_avg_item.append(0)
            y_med_item.append(0)
        if str(d) in list(cdict_auc_item.keys()):
            y_auc_item.append(cdict_auc_item[str(d)])
        else:
            y_auc_item.append(0)
        if str(d) in list(cdict_fix_item.keys()):
            y_fix_item.append(cdict_fix_item[str(d)])
        else:
            y_fix_item.append(0)
        if d in list(quart_ls_item.keys()):
            y_q1_gpitem.append(quart_ls_item[d][0])
            y_q3_gpitem.append(quart_ls_item[d][2])
            y_med_gpitem.append(quart_ls_item[d][1])
        else:
            y_q1_gpitem.append(0)
            y_q3_gpitem.append(0)
            y_med_gpitem.append(0)

    # ============== CREATE PLOTS ============== #
    # store the titles as string and basic layout as a dictionnary
    title_total = "Total sales per year (in 1900 french francs)"
    title_avg_cat = "Average sales per catalogue and per year (in 1900 french francs)"
    title_med_cat = "Median sales price per catalogue per year (in 1900 french francs)"
    title_avg_item = "Average sale price of an item per year (in 1900 french francs)"
    title_med_item = "Median sale price of an item per year (in 1900 french francs)"
    title_cnt = "Number of items for sale per year"
    title_qnt = "Evolution of the price of an item (in 5 year ranges, in quartiles and in 1900 francs)"
    # figure 1 : sum of sales per year
    layout["yaxis"] = {"anchor": "x", "title": {"text": "Total sales"}}
    layout["title"] = title_total
    layout["yaxis_range"] = [0, 75000]  # cut off the excess values
    layout["xaxis_range"] = [1844, 1955]
    # about "marker" : the colorscale values are set to what looks best and can be changed with new data
    fig1 = go.Figure(
        data=[go.Bar(x=x, y=y_total, marker={"color": y_total, "colorscale": scale,
                                             "cauto": False, "cmin": 0.00, "cmax": 65000.00},
                     hovertemplate="<b>Year</b>: %{x}<br><b>Sum of all catalogues' "
                                   + "prices </b>: %{y:.2f} FRF<extra></extra>")],
        layout=go.Layout(layout)
    )
    # figure 2 : average of the sum of sales in a catalogue per year
    layout["yaxis"] = {"anchor": "x", "title": {"text": "Average sales per catalogue"}}
    layout["title"] = title_avg_cat
    layout["yaxis_range"] = [0, 10000]  # cut off the excess values
    layout["xaxis_range"] = [1844, 1955]
    fig2 = go.Figure(
        data=[go.Bar(x=x, y=y_avg_cat, marker={"color": y_avg_cat, "colorscale": scale,
                                               "cauto": False, "cmin": 0.00, "cmax": 7000},
                     hovertemplate="<b>Year</b>: %{x}<br><b>Average sum of prices per catalogue"
                                   + "</b>: %{y:.2f} FRF<extra></extra>")],
        layout=go.Layout(layout)
    )
    # figure 3 : median of the sum of sales in a catalogue per year
    layout["yaxis"] = {"anchor": "x", "title": {"text": "Median sales per catalogue"}}
    layout["title"] = title_med_cat
    layout["yaxis_range"] = [0, 10000]  # cut off the excess values
    layout["xaxis_range"] = [1844, 1955]
    fig3 = go.Figure(
        data=[go.Bar(x=x, y=y_med_cat, marker={"color": y_med_cat, "colorscale": scale,
                                               "cauto": False, "cmin": 0.00, "cmax": 8000},
                     hovertemplate="<b>Year</b>: %{x}<br><b>Median sales per catalogue"
                                   + "</b>: %{y:.2f} FRF<extra></extra>")],
        layout=go.Layout(layout)
    )
    # figure 4 : average price of an item per year
    layout["yaxis"] = {"anchor": "x", "title": {"text": "Average item price"}}
    layout["title"] = title_avg_item
    layout["yaxis_range"] = [0, 32]  # cut off the excess values
    layout["xaxis_range"] = [1844, 1955]
    fig4 = go.Figure(
        data=[go.Bar(x=x, y=y_avg_item, marker={"color": y_avg_item, "colorscale": scale,
                                                "cauto": False, "cmin": 0.00, "cmax": 25},
                     hovertemplate="<b>Year</b>: %{x}<br><b>Average item price</b>: %{y:.2f} FRF<extra></extra>")],
        layout=go.Layout(layout)
    )
    # figure 5 : median price of an item per year
    layout["yaxis"] = {"anchor": "x", "title": {"text": "Median item price"}}
    layout["title"] = title_med_item
    layout["yaxis_range"] = [0, 32]  # cut off the excess values
    fig5 = go.Figure(
        data=[go.Bar(x=x, y=y_med_item, marker={"color": y_med_item, "colorscale": scale,
                                                "cauto": False, "cmin": 0.00, "cmax": 25},
                     hovertemplate="<b>Year</b>: %{x}<br><b>Median item price</b>: %{y:.2f} FRF<extra></extra>")],
        layout=go.Layout(layout)
    )
    # figure 6 : number of fixed price and auction items per year
    layout["yaxis"] = {"anchor": "x", "title": {"text": "Number of items for sale"}}
    layout["title"] = title_cnt
    layout["yaxis_range"] = [0, max(y_auc_item)]  # cut off the excess values
    layout["xaxis_range"] = [1840, 1955]
    fig6 = go.Figure(
        data=[
            go.Bar(x=x, y=y_fix_item, marker={"color": colors["burgundy2"], "opacity": 0.7},
                   hovertemplate="<b>Year</b>: %{x}<br><b>Number of fixed-price "
                                 + "items for sale </b>: %{y}<extra></extra>"),
            go.Bar(x=x, y=y_auc_item, marker={"color": colors["blue"], "opacity": 0.55},
                   hovertemplate="<b>Year</b>: %{x}<br><b>Number of auction items for sale </b>: %{y}<extra></extra>")
        ],
        layout=go.Layout(layout)
    )
    # figure 7 : 1 box chart per 5 year range
    layout["yaxis"] = {"anchor": "x", "title": {"text": "Price of an item (in quantiles)"}}
    layout["title"] = title_qnt
    layout["yaxis_range"] = [0, 80]  # cut off the excess values
    layout["xaxis_range"] = [1840, 1925]
    fig7 = go.Figure(
        data=[go.Box(x=x, q1=y_q1_gpitem, median=y_med_gpitem, q3=y_q3_gpitem,
                     marker={"color": colors["blue"]},
                     fillcolor=colors["cream"],
                     width=4)
              ],
        layout=go.Layout(layout)
    )

    # saving the files ; the file will be called in an iframe using a url_for
    with open(f"{outdir}/fig_IDX_1.html", mode="w") as out:
        fig1.write_html(file=out, full_html=False, include_plotlyjs="cdn", default_width="100%", default_height=275)
    with open(f"{outdir}/fig_IDX_2.html", mode="w") as out:
        fig2.write_html(file=out, full_html=False, include_plotlyjs="cdn", default_width="100%", default_height=275)
    with open(f"{outdir}/fig_IDX_3.html", mode="w") as out:
        fig3.write_html(file=out, full_html=False, include_plotlyjs="cdn", default_width="100%", default_height=275)
    with open(f"{outdir}/fig_IDX_4.html", mode="w") as out:
        fig4.write_html(file=out, full_html=False, include_plotlyjs="cdn", default_width="100%", default_height=275)
    with open(f"{outdir}/fig_IDX_5.html", mode="w") as out:
        fig5.write_html(file=out, full_html=False, include_plotlyjs="cdn", default_width="100%", default_height=275)
    with open(f"{outdir}/fig_IDX_6.html", mode="w") as out:
        fig6.write_html(file=out, full_html=False, include_plotlyjs="cdn", default_width="100%", default_height=275)
    with open(f"{outdir}/fig_IDX_7.html", mode="w") as out:
        fig7.write_html(file=out, full_html=False, include_plotlyjs="cdn", default_width="100%", default_height=275)

    # return
    return figpath














def figmaker_cat(cat_id):
    """
    function to create the figures to be called on the catalogue pages. 2 figures are created:
    - price distribution in the catalogue (violin plot)
    - 10 most expensive items (bar chart)

    the figures are created in 3 steps:
    - data preparation:
      - for figure 1, the price of all items in the catalogue are added to x1
      - for figure 2, the 10 most expensive items are extracted from x1 and used
        to build a dictionary of 10 most expensive items sorted by price (this dict
        is basically a copy of their export_item.json version)
    - preparing the x and y axis: this step only concerts figure 2:
      - build y2 (height of the bars, aka the price of the items)
      - build data for the hover templates
    - creating the figures (the two figures are subplots, i.e. they are subfigures in a
    single figure) and saving them as html files

    the html figures are displayed on the html catalogue pages within an iframe and
    called with a url_for pointing towards that figure
    see the description of figmaker_idx for a few extra details

    :return: figpath (boolean: True if there is price info and a price is created, false if not)
    """
    # ============== DEFINING VARIABLES ============== #
    x1 = []  # x axis of the 1st plot (violin plot): the prices of all items in a catalogue
    x2 = []  # x axis of the 2nd plot: tei:name of the most expensive items
    y2 = []  # y axis of the 2nd plot: top 10 prices
    hovdata = []  # list of lists to pass to fig2's template
    pdict_top = {}  # dictionary mapping to the 10 most expensive item's xml:id their data in export_item.json
    #                 pdict_top can have more than 10 items if several items share the same top prices
    sort_pdict_top = {}  # dictionary to sort pdict_top by item price
    nloop = 0  # count number of loops
    figpath = False  # variable to check if a figure will be created and if a path towards a figure
    #                  will exist ; if there's price info on that catalogue, a figure will be created
    currency = ""

    # ============== PREPARE THE DATA ============== #
    # prepare data for the x1 (the x axis of the first figure)
    for i in js_item:
        if js_item[i]["price"] is not None \
                and re.match(f"{cat_id}_e\d+(_d\d+)?", i):
            if nloop == 0:
                currency = js_item[i]["currency"]
                nloop += 1
            x1.append(js_item[i]["price"])
            figpath = True

    # prepare data for the second figure
    # small safeguard in case there are less than 10 items with a price
    if len(x1) >= 10:
        top_price = sorted(x1)[-10:]  # 10 highest prices prices
    else:
        top_price = sorted(x1)
    for i in js_item:
        if re.match(f"{cat_id}_e\d+(_d\d+)?", i) \
                and js_item[i]["price"] is not None \
                and js_item[i]["price"] in top_price:
            pdict_top[i] = js_item[i]

    # order pdict_top by price
    for p in top_price:
        for k, v in pdict_top.items():
            if p == v["price"]:
                sort_pdict_top[k] = v
    pdict_top = sort_pdict_top

    # ============== BUILD THE X AND Y AXIS ============== #
    # create the x2 axis, y2 axis and data for the hover template
    for v in pdict_top.values():
        y2.append(v["price"])
        x2.append(v["author"]) if v["author"] is not None else x2.append("unknown")
        itlist = []  # list of data on an item to pass to hovdata
        itlist.append(v["author"]) if v["author"] is not None else itlist.append("unknown")
        itlist.append(f"{v['price']} {currency}") if v["price"] is not None else itlist.append("unknown")
        itlist.append(v["date"]) if v["date"] is not None else itlist.append("unknown")
        itlist.append(v["number_of_pages"]) if v["number_of_pages"] is not None else itlist.append("unknown")
        if v["desc"] is not None and len(v["desc"]) <= 90:
            itlist.append(v["desc"])
        elif v["desc"] is not None and len(v["desc"]) > 90:
            itlist.append(v["desc"][:90] + "[...]")
        else:
            itlist.append("unknown")
        hovdata.append(itlist)
    # update x2 if there are duplicates
    # if several items have the same title, plotly treats them as a single item and stacks them up. to
    # avoid this, check if there are duplicates ; if there are duplicates, rename the duplicate titles
    # by adding a number in parentheses: "Title (1)" for the first one, "Title (2)" for the second...
    if len(set(x2)) != len(x2):
        duplicates = [t for t in x2 if x2.count(t) > 1]
        tlist = []  # list to temporarily store the titles for fig2 (tlist = "title list")
        dupldict = {}  # mapping of title to the number of duplicates
        for t in x2:
            if t not in list(dupldict.keys()):
                dupldict[t] = 1
            else:
                dupldict[t] += 1
            if t in duplicates:
                tlist.append(f"{t} ({dupldict[t]})")
            else:
                tlist.append(t)
        x2 = tlist

    # ============== CREATE PLOTS ============== #
    if currency == "FRF":
        currinfo = "in french francs"
    elif currency == "USD":
        currinfo = "in US dollars"
    elif currency == "GBP":
        currinfo = "in pounds"
    else:
        currinfo = "None"
    layout = {
        "paper_bgcolor": colors["cream"],
        "plot_bgcolor": colors["cream"],
        "margin": {"l": 5, "r": 5, "t": 30, "b": 30},
        "showlegend": False,
    }

    fig = make_subplots(
        rows=2, cols=1,
        vertical_spacing=0.15,
        row_heights=[0.6, 0.4],
        subplot_titles=(f"Distribution of the prices in the catalogue ({currinfo})",
                        f"Ten most expensive items ({currinfo})")
    )
    # subplot 1: violin plot showing the price distribution in the catalogue, with quartiles and mean prices
    fig.add_trace(
        go.Violin(
            x=x1, meanline={"visible": True, "color": colors["blue"]}, width=1,
            marker={"color": colors["burgundy2"],
                    "outliercolor": colors["blue"]},
            box={"visible": True, "line": {"color": colors["blue"]}},
            fillcolor=colors["cream"]
        ),
        row=1, col=1
    )
    # subplot 2: bar chart of the most expensive items in the catalogue
    fig.add_trace(
        go.Bar(y=y2, x=x2, marker={"color": y2, "colorscale": scale},
               hovertemplate="<b>Author or document's title</b>: %{customdata[0]}<br>"
                             + "<b>Price</b>: %{customdata[1]}<br>"
                             + "<b>Date of the document</b>: %{customdata[2]}<br>"
                             + "<b>Number of pages</b>: %{customdata[3]}<br>"
                             + "<b>Description</b>: %{customdata[4]}"
                             + "<extra></extra>",
               customdata=hovdata),
        row=2, col=1
    )
    # layout
    fig.update_layout(layout)
    fig["layout"]["xaxis"]["title"] = "Price (in french francs)"
    fig["layout"]["yaxis"]["title"] = "Proportion of items"
    fig["layout"]["yaxis"]["showticklabels"] = False
    fig["layout"]["yaxis2"]["title"] = "Price"

    # saving the files ; the file will be called in an iframe using a url_for
    with open(f"{outdir}/fig_{cat_id}.html", mode="w") as out:
        fig.write_html(file=out, full_html=False, include_plotlyjs="cdn", default_width="100%", default_height=650)

    # return : if there is price data, figpath is true and a path to a figure for that catalogue will be available
    return figpath


# FOR FIGMAKER_CAT IF THE FIGURES ARE SAVED IN TWO SEPARATE FILES
#    # figure 1: violin plot showing the price distribution in the catalogue, with quarties and mean prices
#    fig1 = go.Figure(
#        data=go.Violin(x=x1, meanline={"visible": True, "color": colors["blue"]}, width=1,
#                       marker={"color": colors["burgundy2"],
#                               "outliercolor": colors["blue"]},
#                       box={"visible": True, "line": {"color": colors["blue"]}},
#                       fillcolor=colors["cream"]),
#        layout=go.Layout(layout)
#    )
#    # figure 2: bar chart of the most expensive items in the catalogue
#    layout["xaxis_tickangle"] = -25
#    fig2 = go.Figure(
#        data=go.Bar(y=y2, x=x2, marker={"color": y2, "colorscale": scale},
#                    hovertemplate="<b>Author or document's title</b>: %{customdata[0]}<br>"
#                                  + "<b>Date of the document</b>: %{customdata[1]}<br>"
#                                  + "<b>Number of pages</b>: %{customdata[2]}<br>"
#                                  + "<b>Description</b>: %{customdata[3]}",
#                    customdata=hovdata),
#        layout=go.Layout(layout)
#    )
#
#    # saving the files ; the file will be called in an iframe using a url_for
#    with open(f"{outdir}/fig_{cat_id}_1.html", mode="w") as out:
#        fig1.write_html(file=out, full_html=False, include_plotlyjs="cdn", default_width="100%", default_height=275)
#    with open(f"{outdir}/fig_{cat_id}_2.html", mode="w") as out:
#        fig2.write_html(file=out, full_html=False, include_plotlyjs="cdn", default_width="100%", default_height=275)


# https://plotly.com/python-api-reference/generated/plotly.colors.html
# https://plotly.com/python/reference/layout/coloraxis/
import pandas as pd
import plotly.express as px

def bar_chart(df, x, y, title):
    data = df.groupby(x)[y].mean().reset_index()

    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title
    )

    return fig


def line_chart(df, x, y, title):
    data = df.groupby(x)[y].mean().reset_index()

    fig = px.line(
        data,
        x=x,
        y=y,
        title=title
    )

    return fig

def histogram(df, column, title):
    fig = px.histogram(
        df,
        x=column,
        title=title
    )

    return fig

def scatter_chart(df, x, y, color=None, title=""):
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        title=title
    )

    return fig

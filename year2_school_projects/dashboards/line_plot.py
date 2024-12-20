'''
File: line_plot.py
Description: CHANGE
'''
# Sheryl and Aria
import plotly.express as px

def plot_city(df, date_range, city_feature, selected_city):

    fig = px.line(df, x='datetime', y=city_feature, color = "name")
    title = f"{city_feature} Over Time in {selected_city}"
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=city_feature,
        title = title
    )
    return fig

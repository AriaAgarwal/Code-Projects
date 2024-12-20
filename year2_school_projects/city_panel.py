'''
File: citypanel_api.py
Description: This file calls the city_api.py file, provides widgets for the user to select features,
creates a plot and a dataframe through binding the user selection, and creates an interactive dashboard.
'''

# Importing necessary libraries and panel extension
import panel as pn
from city_api import CITY_API
import datetime
import line_plot as ploty
pn.extension()

# Initialize city API
city_api = CITY_API()

# Loading data for 4 cities:
city_api.load_city(("boston_weather.csv", "bloomington_weather.csv", "cupertino_weather.csv", "pasadena_weather.csv"))

# Sheryl: A select feature that allows user to select the feature displayed (ie temp max, temp min, humidity, etc.)
weather_feature_select = pn.widgets.Select(name='Select Weather Feature', options=city_api.get_city_features())

# Sheryl: Date range picker that allows the user to select dates to display
# Referenced: https://panel.holoviz.org/reference/widgets/DatetimeRangePicker.html
date_range = pn.widgets.DateRangePicker(
    name='Select Date Range',
    start=datetime.date(2023, 10, 2),
    end=datetime.date(2024, 10, 1),
    value=(datetime.date(2023, 10, 2), datetime.date(2024, 10, 1))
)

# Sheryl: Check box feature that allows the user to select cities to display
# Referenced: https://panel.holoviz.org/reference/widgets/CheckBoxGroup.html
city_options = ['Boston', 'Bloomington', 'Cupertino', 'Pasadena']
city_checkbox = pn.widgets.CheckBoxGroup(name='Select Cities to Display', options=city_options)

# Abigail: Markdown descriptions for the widgets (for easier visibility of selection)
date_range_display = pn.pane.Markdown(f'Selected Date Range: {date_range.value}')
weather_feature_display = pn.pane.Markdown(f'Selected Weather Feature: {weather_feature_select.value}')
city_display = pn.pane.Markdown(f'Selected Cities: {city_checkbox.value}')

# Abigail: Updating display based on user selection
def update_markdown(event):
    date_range_display.object = f'Date range selected: {date_range.value}'
    weather_feature_display.object = f'Weather feature selected: {weather_feature_select.value}'
    city_display.object = f'Selected Cities: {city_checkbox.value}'

# Abigail: Binding the features to the update markdown function
date_range.param.watch(update_markdown, 'value')
weather_feature_select.param.watch(update_markdown, 'value')
city_checkbox.param.watch(update_markdown, 'value')


# Aria: Creating the plot based on user selection (later displayed on tab 1)
def get_plot(weather_feature_select, city_checkbox, date_range):
    selected_city = city_checkbox
    plot_df = city_api.get_user_filtered_features(weather_feature_select, date_range, selected_city)
    fig = ploty.plot_city(plot_df, date_range, weather_feature_select, selected_city)
    return fig

# Sheryl: Creating a dataframe of the user selection (later displayed on tab 2)
def dataframe_view(feature, city_checkbox, date_range):
    df_view = city_api.get_user_filtered_features(feature, date_range, city_checkbox)
    return df_view

# Aria and Sheryl Binding inorder to display the plot and dataframe on dashboard
plot = pn.bind(get_plot, weather_feature_select, city_checkbox, date_range)
df_view = pn.bind(dataframe_view, feature=weather_feature_select, date_range=date_range, city_checkbox=city_checkbox)
plot_panel = pn.Column(plot)

# Abigail: Cards for widgets
date_card = pn.Card(
    date_range,
    date_range_display,
)
city_card = pn.Card(
    city_checkbox,
    city_display
)
weather_feature_card = pn.Card(
    weather_feature_select,
    weather_feature_display
)

# Abigail: Creating the layout of the dashboard, referencing to gadexplorer.py code
layout = pn.template.FastListTemplate(
    title="Weather Analysis",
    sidebar=[
        city_card,
        date_card,
        weather_feature_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Graph", plot),
            ("Dataframe Input", df_view),
            active=0
        )
    ],
    header_background='#FFB6C1'
).servable()
layout.show()




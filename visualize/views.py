from django.shortcuts import render, redirect

# added
import json
from django.http import HttpResponse
import pandas as pd
import numpy as np
from .models import Dengue
from io import BytesIO, StringIO
import base64
import matplotlib
import matplotlib.pyplot as plt
import io
import datetime, calendar
import plotly.express as px

# Create your views here.

# do not send an HTML page
# send back data in a form of JSON


def index(request):
    return render(request, 'visualize/index.html')

def home(request):
    return render(request, 'visualize/index.html')

# year (display ang selected_year sa dropdown)
# specific date
# all input fields
# quick: highest total number of cases (location)
# quick: highest total number of deaths (location)
# quick: highest total number of cases (specific date)
# quick: highest total number of deaths (specific date)


# function for data preprocessing
def clean_data(df):
    df = df.dropna(subset=['loc'])
    df['loc'] = df['loc'].replace('SISQUIJOR', 'SIQUIJOR')
    df['cases'] = df['cases'].fillna(0)
    df['deaths'] = df['deaths'].fillna(0)
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
    df['year'] = pd.to_datetime(df['date'], errors='coerce').dt.year
    df['month'] = pd.to_datetime(df['date'], errors='coerce').dt.month
    return df

# function to generate narrations
def generate_narration(max_cases_year, max_deaths_year, max_cases_month, max_deaths_month, selected_location, selected_month, selected_year):
    narration = "The graph illustrates Dengue cases and deaths"

    if selected_month:
        narration += f" in the month of {selected_month}"

    if selected_location:
        narration += f" in {selected_location}"

    if selected_year:
        narration = "The graph illustrates the monthly Dengue cases and deaths"  # Updated line

        if selected_month:
            narration += f" in the month of {selected_month}"
        else:
            narration += " across all months"

        narration += f" in the year {selected_year}."

        if max_cases_month:
            narration += f"<br><br>The month with the highest total number of cases is {max_cases_month}"

        if max_deaths_month:
            narration += f"<br><br>The month with the highest total number of deaths is {max_deaths_month}"

    if not selected_year:
        if max_cases_year != 0:
            narration += f"<br><br>The year with the highest total number of cases is {max_cases_year}"

        if max_deaths_year != 0:
            narration += f"<br><br>The year with the highest total number of deaths is {max_deaths_year}"

    narration += ".<br><br>"
    return narration


# Function to create chart (line chart) for overall stats, when user input is empty
def create_chart_overall_stats(location_stats, title, height=500):
    fig = px.line(location_stats, x='year', y=['cases', 'deaths'], labels={'year': 'Year', 'value': 'Count'},
                  title=title, markers=True)
    fig.update_xaxes(tickmode='array', tickvals=location_stats['year'].unique())
    fig.update_layout(xaxis_title='Year', yaxis_title='Count', legend_title='Legend', height=height)
    fig.update_layout(title={'text': title, 'x': 0.5})
    return fig.to_html()

# Function to create chart (line chart) for selected year and month and location
def create_chart_selected_year_month(location_stats, title, height=500):
    # Convert month numbers to month names
    location_stats['month'] = location_stats['month'].apply(lambda x: calendar.month_name[x])

    fig = px.line(location_stats, x='month', y=['cases', 'deaths'], labels={'month': 'Month', 'value': 'Count'},
                  title=title, markers=True)
    fig.update_layout(xaxis_title='Month', yaxis_title='Count', legend_title='Legend', height=height)
    fig.update_layout(title={'text': title, 'x': 0.5})
    return fig.to_html()

def project1(request):
    dengue_data = Dengue.objects.all()
    df = pd.DataFrame(list(dengue_data.values()))
    df = clean_data(df)

    locations = sorted(df['loc'].unique())
    unique_years = sorted(df['year'].unique())
    unique_months = sorted(df['date'].apply(lambda x: x.strftime('%B')).unique(),
                            key=lambda x: datetime.datetime.strptime(x, '%B'))

    selected_location = request.POST.get('location')
    selected_month = request.POST.get('month')
    selected_year = request.POST.get('year')

    if selected_location and selected_month:
        df_filtered = df[(df['loc'] == selected_location) & (df['month'] == unique_months.index(selected_month) + 1)]
    elif selected_month:
        df_filtered = df[df['month'] == unique_months.index(selected_month) + 1]
    elif selected_location:
        df_filtered = df[df['loc'] == selected_location]
    elif selected_year:
        df_filtered = df[df['year'] == int(selected_year)]
    else:
        df_filtered = df

    # Separate location_stats based on whether a specific year is selected
    if selected_year:
        location_stats = df_filtered.groupby(['year', 'month']).agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()

        max_cases_month = location_stats.loc[location_stats['cases'].idxmax()]['month']
        max_deaths_month = location_stats.loc[location_stats['deaths'].idxmax()]['month']
        
        # Convert month number to month name
        max_cases_month = datetime.date(2022, int(max_cases_month), 1).strftime('%B')
        max_deaths_month = datetime.date(2022, int(max_deaths_month), 1).strftime('%B')
    else:
        location_stats = df_filtered.groupby('year').agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()
        max_cases_month = None
        max_deaths_month = None

    max_cases_year = int(location_stats.loc[location_stats['cases'].idxmax()]['year'])
    max_deaths_year = int(location_stats.loc[location_stats['deaths'].idxmax()]['year'])

    narration = generate_narration(max_cases_year, max_deaths_year, max_cases_month, max_deaths_month, selected_location, selected_month, selected_year)

    # Create chart based on the selected year and month and location
    if selected_year:
        title = f'Dengue Cases and Deaths in the Year {selected_year}'
        chart_html = create_chart_selected_year_month(location_stats, title)
    else:
        title = f'Dengue Cases and Deaths in {selected_location} Over the Years' if selected_location else f'Dengue Cases and Deaths in the month of {selected_month} Over the Years' if selected_month else 'Dengue Cases and Deaths Over the Years'
        chart_html = create_chart_overall_stats(location_stats, title)

    context = {
        'dengue_data': df.head(5).to_dict(orient='records'),
        'chart_html': chart_html,
        'narration': narration,
        'unique_years': unique_years,
        'unique_months': unique_months,
        'locations': locations,
        'selected_location': selected_location,
        'selected_month': selected_month,
        'selected_year': selected_year,
    }

    return render(request, 'visualize/project1.html', context)

# Mapping
def project2(request):
    return render(request, 'visualize/project2.html')


# Bonus
def project3(request):
    return render(request, 'visualize/project3.html')

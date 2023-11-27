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
import datetime
import plotly.express as px

# Create your views here.

# do not send an HTML page
# send back data in a form of JSON


def index(request):
    return render(request, 'visualize/index.html')

def home(request):
    return render(request, 'visualize/index.html')

# condition kung 0 ang highest
# ang x date
def project1(request):
    # Load data from the Dengue model
    dengue_data = Dengue.objects.all()

    # Create a DataFrame from the Django QuerySet
    df = pd.DataFrame(list(dengue_data.values()))

    # Drop rows with empty 'loc'
    df = df.dropna(subset=['loc'])

    # Replace 'SISQUIJOR' with 'SIQUIJOR' in the 'loc' column
    df['loc'] = df['loc'].replace('SISQUIJOR', 'SIQUIJOR')

    # Replace empty values in 'cases' and 'deaths' with 0
    df['cases'] = df['cases'].fillna(0)
    df['deaths'] = df['deaths'].fillna(0)

    # Convert 'date' column to pandas datetime type and remove the time component
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

    # Create a new 'year' column by extracting the year from the 'date' column
    df['year'] = pd.to_datetime(df['date'], errors='coerce').dt.year

    # Create a new 'year' column by extracting the year from the 'date' column
    df['month'] = pd.to_datetime(df['date'], errors='coerce').dt.month

    # Capture unique locations of the 'loc' column
    locations = sorted(df['loc'].unique())

    # Capture unique years and months for dropdown options
    unique_years = sorted(df['year'].unique())
    unique_months = sorted(df['date'].apply(lambda x: x.strftime('%B')).unique(),
                            key=lambda x: datetime.datetime.strptime(x, '%B'))

    print(df.head(5))
    
    # narration
    # narration = "The graph illustrates yearly trends of Dengue cases and deaths over the years. "

    # Handle user input
    selected_location = request.POST.get('location')
    selected_month = request.POST.get('month')

    if selected_location and selected_month:
        # Filter data based on the selected location and month
        df_filtered = df[(df['loc'] == selected_location) & (df['month'] == unique_months.index(selected_month) + 1)]

        # Group data by year and calculate the sum of cases and deaths
        location_stats = df_filtered.groupby('year').agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()

        max_cases_year = location_stats.loc[location_stats['cases'].idxmax()]['year']
        max_deaths_year = location_stats.loc[location_stats['deaths'].idxmax()]['year']

        max_cases_year = int(max_cases_year)
        max_deaths_year = int(max_deaths_year)

        # Create a narration about the selected location
        narration = (
            f"The graph illustrates Dengue cases and deaths in the month of {selected_month} in {selected_location} across years.<br><br>"
            f"The year with the highest total number of cases is {max_cases_year}.<br><br>"
            f"The year with the highest total number of deaths is {max_deaths_year}."
        )

        # Create Plotly Express line chart
        fig = px.line(location_stats, x='year', y=['cases', 'deaths'], labels={'year': 'Year', 'value': 'Count'},
                        title=f'Dengue Cases and Deaths in {selected_location} Over the Years', markers=True)
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Count',
            legend_title='Legend',
            title={'text': f'Dengue Cases and Deaths in {selected_location} Over the Years', 'x': 0.5}
        )

        # Convert the Plotly Express chart to HTML
        chart_html = fig.to_html()

    # Perform data filtering based on the selected month
    elif selected_month:
        # Filter data based on the selected month across all locations and years
        df_filtered = df[df['month'] == unique_months.index(selected_month) + 1]

        # Group data by year and calculate the sum of cases and deaths
        location_stats = df_filtered.groupby('year').agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()

        max_cases_year = location_stats.loc[location_stats['cases'].idxmax()]['year']
        max_deaths_year = location_stats.loc[location_stats['deaths'].idxmax()]['year']

        max_cases_year = int(max_cases_year)
        max_deaths_year = int(max_deaths_year)

        # Create a narration about the selected month
        narration = (
            f"The graph illustrates Dengue cases and deaths in the month of {selected_month} across years.<br><br>"
            f"The year with the highest total number of cases is {max_cases_year}.<br><br>"
            f"The year with the highest total number of deaths is {max_deaths_year}."
        )

        # Create Plotly Express line chart
        fig = px.line(location_stats, x='year', y=['cases', 'deaths'], labels={'year': 'Year', 'value': 'Count'},
                        title=f'Dengue Cases and Deaths in the month of {selected_month} Over the Years', markers=True)
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Count',
            legend_title='Legend',
            title={'text': f'Dengue Cases and Deaths in the month of {selected_month} Over the Years', 'x': 0.5}
        )

        # Convert the Plotly Express chart to HTML
        chart_html = fig.to_html()

    # Perform data filtering based on the selected location
    elif selected_location is not None and selected_location != "":
        df_location = df[df['loc'] == selected_location]

        # Group data by year and calculate the sum of cases and deaths
        location_stats = df_location.groupby('year').agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()

        max_cases_year = location_stats.loc[location_stats['cases'].idxmax()]['year']
        max_deaths_year = location_stats.loc[location_stats['deaths'].idxmax()]['year']

        max_cases_year = int(max_cases_year)
        max_deaths_year = int(max_deaths_year)

        # Create a narration about the selected location
        narration = (
            f"The graph illustrates Dengue cases and deaths in {selected_location} across years.<br><br>"
            f"The year with the highest total number of cases is {max_cases_year}.<br><br>"
            f"The year with the highest total number of deaths is {max_deaths_year}."
        )

        # Create Plotly Express line chart
        fig = px.line(location_stats, x='year', y=['cases', 'deaths'], labels={'year': 'Year', 'value': 'Count'},
                        title=f'Dengue Cases and Deaths in {selected_location} Over the Years', markers=True)
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Count',
            legend_title='Legend',
            title={'text': f'Dengue Cases and Deaths in {selected_location} Over the Years', 'x': 0.5}
        )

        # Convert the Plotly Express chart to HTML
        chart_html = fig.to_html()

    else:
        # By default, show overall stats if the input fields are empty
        overall_stats = df.groupby('year').agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()

        # Print the overall sum of cases and deaths each year
        print("Overall Sum of Cases and Deaths Each Year:")
        print(overall_stats)

        # Find the year with the highest total number of cases and deaths
        max_cases_year = overall_stats.loc[overall_stats['cases'].idxmax()]['year']
        max_deaths_year = overall_stats.loc[overall_stats['deaths'].idxmax()]['year']

        # Remove the decimal point from the year values
        max_cases_year = int(max_cases_year)
        max_deaths_year = int(max_deaths_year)

        # Create a narration about the year with the highest cases and deaths
        narration = (
            "The graph illustrates yearly trends of Dengue cases and deaths over the years.<br><br>"
            f"The year with the highest total number of cases is {max_cases_year}.<br><br>"
            f"The year with the highest total number of deaths is {max_deaths_year}."
        )

        # Create Plotly Express line chart
        fig = px.line(overall_stats, x='year', y=['cases', 'deaths'], labels={'year': 'Year', 'value': 'Count'},
                    title='Dengue Cases and Deaths Over the Years', markers=True)
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Count',
            legend_title='Legend',
            title={'text': 'Dengue Cases and Deaths Over the Years', 'x': 0.5}
        )

        # Convert the Plotly Express chart to HTML
        chart_html = fig.to_html()


    # Pass data to the template
    context = {
        'dengue_data': df.head(5).to_dict(orient='records'),
        'chart_html': chart_html,
        'narration': narration,
        'unique_years': unique_years,
        'unique_months': unique_months,
        'locations': locations,
        'selected_location': selected_location,
        'selected_month': selected_month,
    }

    return render(request, 'visualize/project1.html', context)


# Mapping
def project2(request):
    return render(request, 'visualize/project2.html')


# Bonus
def project3(request):
    return render(request, 'visualize/project3.html')

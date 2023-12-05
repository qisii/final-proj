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
from django.contrib import messages



# Create your views here.

# do not send an HTML page
# send back data in a form of JSON


def index(request):
    return render(request, 'visualize/index.html')

def home(request):
    return render(request, 'visualize/index.html')

# function for data preprocessing
def clean_data(df):
    df = df.dropna(subset=['loc'])
    df['loc'] = df['loc'].replace('SISQUIJOR', 'SIQUIJOR')
    df['loc'] = df['loc'].replace(' CAGAYAN DE ORO CITY', 'CAGAYAN DE ORO CITY')
    df['loc'] = df['loc'].replace(' NEGROS ORIENTAL', 'NEGROS ORIENTAL')
    df['cases'] = df['cases'].fillna(0)
    df['deaths'] = df['deaths'].fillna(0)
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
    df['year'] = pd.to_datetime(df['date'], errors='coerce').dt.year
    df['month'] = pd.to_datetime(df['date'], errors='coerce').dt.month
    return df

# function to generate narrations
def generate_narration(max_cases_year, max_deaths_year, max_cases_month, max_deaths_month, max_cases_date, max_deaths_date, max_cases_location, max_deaths_location, selected_location, selected_month, selected_year, selected_date, selected_region, has_data):
    narration = "The graph illustrates the Total Dengue cases and deaths"

    if selected_month:
        narration += f" in the month of <b>{selected_month}</b>"

    if selected_location:
        narration += f" in <b>{selected_location}</b>"
    elif selected_region:
        narration += f" in <b>{selected_region}</b>"

    narration += " across years."

    if selected_date:
        
        if has_data == True:
            narration = "The graph illustrates Dengue cases and deaths"

            selected_date = pd.to_datetime(selected_date).strftime('%B %d, %Y')
            narration += f" on <b>{selected_date}</b>"

            if selected_location:
                narration += f" in <b>{selected_location}</b>."
            elif selected_region:
                narration += f" in <b>{selected_region}</b>"
            else:
                narration += " across locations."

        if has_data == False:
            selected_date = pd.to_datetime(selected_date).strftime('%B %d, %Y')
            narration = f"No data available for <b>{selected_date}</b>"

            if selected_location:
                narration += f" in <b>{selected_location}</b>."
            elif selected_region:
                narration += f" in <b>{selected_region}</b>"
            else:
                narration += " across locations."

    if selected_year:
        narration = "The graph illustrates the monthly Dengue cases and deaths"

        if selected_month:
            narration += f" in the month of <b>{selected_month}</b>"
        else:
            narration += " across all months"
        
        if selected_location:
            narration += f" in <b>{selected_location}</b>"
        elif selected_region:
            narration += f" in <b>{selected_region}</b>"

        narration += f" in the year <b>{selected_year}.</b>"

        if max_cases_month:
            narration += f"<br><br>The month with the highest total number of cases is <b>{max_cases_month}</b>."

        if max_deaths_month:
            narration += f"<br><br>The month with the highest total number of deaths is <b>{max_deaths_month}</b>."
        
        if max_cases_date:
            max_cases_date = pd.to_datetime(max_cases_date).strftime('%B %d, %Y')
            narration += f"<br><br>The date with the highest total number of cases is <b>{max_cases_date}</b>."

        if max_deaths_date:
            max_deaths_date = pd.to_datetime(max_deaths_date).strftime('%B %d, %Y')
            narration += f"<br><br>The date with the highest total number of deaths is <b>{max_deaths_date}</b>."\
        
        if max_cases_location:
            narration += f"<br><br>The location with the highest total number of cases is <b>{max_cases_location}</b>."

        if max_deaths_location:
            narration += f"<br><br>The location with the highest total number of deaths is <b>{max_deaths_location}</b>."

    if not selected_year:
        if max_cases_year:
            narration += f"<br><br>The year with the highest total number of cases is <b>{max_cases_year}</b>."

        if max_deaths_year:
            narration += f"<br><br>The year with the highest total number of deaths is <b>{max_deaths_year}</b>."

        if max_cases_location:
            narration += f"<br><br>The location with the highest total number of cases is <b>{max_cases_location}</b>."

        if max_deaths_location:
            narration += f"<br><br>The location with the highest total number of deaths is <b>{max_deaths_location}</b>."

    narration += "<br>"
    return narration

# Function to create chart (line chart) for overall stats, when user input is empty
def create_chart_overall_stats(stats, title, height=490):
    fig = px.line(stats, x='year', y=['cases', 'deaths'], labels={'year': 'Year', 'value': 'Count'},
                  title=title, markers=True)
    fig.update_xaxes(tickmode='array', tickvals=stats['year'].unique())
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(gridcolor='#F2F3F4')
    fig.update_yaxes(gridcolor='#F2F3F4')
    fig.update_layout(xaxis_title='Year', yaxis_title='Count', legend_title='Legend', height=height)
    fig.update_layout(title={'text': title, 'x': 0.5})
    return fig.to_html()

# Function to create chart (line chart) for months
def create_chart_x_month(stats, title, height=490):
    # Convert month numbers to month names
    stats['month'] = stats['month'].apply(lambda x: calendar.month_name[x])

    fig = px.line(stats, x='month', y=['cases', 'deaths'], labels={'month': 'Month', 'value': 'Count'},
                  title=title, markers=True)
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')              
    fig.update_layout(xaxis_title='Month', yaxis_title='Count', legend_title='Legend', height=height)
    fig.update_xaxes(gridcolor='#F2F3F4')
    fig.update_yaxes(gridcolor='#F2F3F4')
    fig.update_layout(title={'text': title, 'x': 0.5})
    return fig.to_html()

# Function to create chart (line chart) for dates
def create_chart_x_date(stats, title, selected_date=None, height=490):
    # Convert month numbers to month names
    stats['month'] = stats['month'].apply(lambda x: calendar.month_name[x])

    fig = px.line(stats, x='date', y=['cases', 'deaths'], labels={'date': 'Date', 'value': 'Count'},
                  title=title, markers=True)

    if selected_date:
        # Highlight selected date with a larger marker
        selected_date_index = stats[stats['date'] == selected_date].index
        fig.update_traces(marker=dict(size=[20 if i in selected_date_index else 7 for i in range(len(stats))]))

    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(xaxis_title='Date', yaxis_title='Count', legend_title='Legend', height=height)
    fig.update_xaxes(gridcolor='#F2F3F4')
    fig.update_yaxes(gridcolor='#F2F3F4')
    fig.update_layout(title={'text': title, 'x': 0.5})
    return fig.to_html()

def create_chart_x_location(stats, title, height=490):
    fig = px.line(stats, x='loc', y=['cases', 'deaths'], labels={'loc': 'Location', 'value': 'Count'},
                  title=title, markers=True)
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')              
    fig.update_layout(xaxis_title='Location', yaxis_title='Count', legend_title='Legend', height=height)
    fig.update_xaxes(gridcolor='#F2F3F4')
    fig.update_yaxes(gridcolor='#F2F3F4')
    fig.update_layout(title={'text': title, 'x': 0.5})
    return fig.to_html()

# Function to create chart (two bar chart)

# function for the dengue data visualization using filters
def project1(request):
    dengue_data = Dengue.objects.all()
    df = pd.DataFrame(list(dengue_data.values()))
    df = clean_data(df)

    # values for the dropdowns
    locations = sorted(df['loc'].unique())
    regions = sorted(df['region'].unique())
    unique_years = sorted(df['year'].unique())
    unique_months = sorted(df['date'].apply(lambda x: x.strftime('%B')).unique(),
                            key=lambda x: datetime.datetime.strptime(x, '%B'))
                            
    # user inputs
    selected_location = request.POST.get('location')
    selected_month = request.POST.get('month')
    selected_year = request.POST.get('year')
    selected_region = request.POST.get('region')
    selected_date = request.POST.get('date')

    # handle user input combination
    if (selected_date and selected_year and selected_month) or (selected_location and selected_region):
        messages.warning(request, "Invalid selected filters. Please try again.")
        chart_html = ''
        narration = f"<b>No data available</b>"
        if selected_date:
            selected_month = ''
            selected_year = ''
    elif (selected_date and (selected_year or selected_month)) or (selected_location and selected_region):
        messages.warning(request, "Invalid selected filters. Please try again.")
        chart_html = ''
        narration = f"<b>No data available</b>"
        if selected_date:
            selected_month = ''
            selected_year = ''
    else:
        # handle user inputs
        # filter dataframe before calculating stats(total cases and deaths)
        if selected_month and selected_year:
            if selected_location:
                df_filtered = df[(df['loc'] == selected_location) & (df['month'] == unique_months.index(selected_month) + 1) & (df['year'] == int(selected_year))]
            elif selected_region:
                df_filtered = df[(df['region'] == selected_region) & (df['month'] == unique_months.index(selected_month) + 1) & (df['year'] == int(selected_year))]
            else:
                df_filtered = df[(df['month'] == unique_months.index(selected_month) + 1) & (df['year'] == int(selected_year))]
        elif selected_date:
            selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d').date()
            selected_month_date = selected_date.strftime('%B')
            selected_year_date = selected_date.year
            if selected_location:
                df_filtered = df[(df['month'] == unique_months.index(selected_month_date) + 1) & (df['year'] == int(selected_year_date)) & (df['loc'] == selected_location)]           
            elif selected_region:
                df_filtered = df[(df['month'] == unique_months.index(selected_month_date) + 1) & (df['year'] == int(selected_year_date)) & (df['region'] == selected_region)]
            else:
                df_filtered = df[(df['month'] == unique_months.index(selected_month_date) + 1) & (df['year'] == int(selected_year_date))]
        elif selected_year:
            if selected_location:
                df_filtered = df[(df['loc'] == selected_location) & (df['year'] == int(selected_year))]
            elif selected_region:
                df_filtered = df[(df['region'] == selected_region) & (df['year'] == int(selected_year))]
            else:
                df_filtered = df[df['year'] == int(selected_year)]
        elif selected_month:
            if selected_location:
                df_filtered = df[(df['loc'] == selected_location) & (df['month'] == unique_months.index(selected_month) + 1)]
            elif selected_region:
                df_filtered = df[(df['region'] == selected_region) & (df['month'] == unique_months.index(selected_month) + 1)]
            else:
                df_filtered = df[df['month'] == unique_months.index(selected_month) + 1]
        elif selected_region:
            df_filtered = df[df['region'] == selected_region]
        elif selected_location:
            df_filtered = df[df['loc'] == selected_location]
        else:
            df_filtered = df

        # Separate stats based on whether a specific request is selected
        # stats => filtered data frame with total cases and deaths
        if selected_year and selected_month:
            if selected_region:
                stats = df_filtered.groupby('loc').agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()

                if not stats.empty:
                    # Find the location with the maximum total cases and deaths across all locations within the selected region
                    max_cases_location = stats.loc[stats['cases'].idxmax(), 'loc'] if stats['cases'].max() > 0 else ''
                    max_deaths_location = stats.loc[stats['deaths'].idxmax(), 'loc'] if stats['deaths'].max() > 0 else ''

                    title = f'Dengue Cases and Deaths in {selected_region}' + (f' for {selected_year}' if selected_year else '')
                    chart_html = create_chart_x_location(stats, title) if not stats.empty else ''
            else:
                stats = df_filtered.groupby(['year', 'month', 'date']).agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()
                max_cases_month = None
                max_deaths_month = None
                max_cases_location = None
                max_deaths_location = None
                has_data = None

                if not stats.empty:
                    max_cases_date = stats.loc[stats['cases'].idxmax()]['date'] if stats['cases'].max() > 0 else ''
                    max_deaths_date = stats.loc[stats['deaths'].idxmax()]['date'] if stats['deaths'].max() > 0 else ''
                    
                    # Convert date to a readable format
                    max_cases_date = max_cases_date.strftime('%Y-%m-%d') if max_cases_date else ''
                    max_deaths_date = max_deaths_date.strftime('%Y-%m-%d') if max_deaths_date else ''

                title = f'Dengue Cases and Deaths for {selected_month} {selected_year}' + (f' in {selected_location}' if selected_location else '')
                chart_html = create_chart_x_date(stats, title) if not stats.empty else ''
        elif selected_year:
            if selected_region:
                stats = df_filtered.groupby('loc').agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()

                if not stats.empty:
                    # Find the location with the maximum total cases and deaths across all locations within the selected region
                    max_cases_location = stats.loc[stats['cases'].idxmax(), 'loc'] if stats['cases'].max() > 0 else ''
                    max_deaths_location = stats.loc[stats['deaths'].idxmax(), 'loc'] if stats['deaths'].max() > 0 else ''

                    title = f'Dengue Cases and Deaths in {selected_region}' + (f' for {selected_year}' if selected_year else '')
                    chart_html = create_chart_x_location(stats, title) if not stats.empty else ''
            else:
                stats = df_filtered.groupby(['year', 'month']).agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()
                max_cases_date = None
                max_deaths_date = None
                max_cases_location = None
                max_deaths_location = None
                has_data = None

                if not stats.empty:
                    max_cases_month = stats.loc[stats['cases'].idxmax()]['month'] if stats['cases'].max() > 0 else ''
                    max_deaths_month = stats.loc[stats['deaths'].idxmax()]['month'] if stats['deaths'].max() > 0 else ''
                    
                    # Convert month number to month name
                    max_cases_month = datetime.date(2022, int(max_cases_month), 1).strftime('%B')
                    max_deaths_month = datetime.date(2022, int(max_deaths_month), 1).strftime('%B')

                title = f'Dengue Cases and Deaths in the Year {selected_year}' + (f' in {selected_location}' if selected_location else '')
                chart_html = create_chart_x_month(stats, title) if not stats.empty else ''
        elif selected_date:
            if selected_region:
                stats = df_filtered.groupby(['year', 'month', 'date']).agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()
            else:
                stats = df_filtered.groupby(['year', 'month', 'date']).agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()

            if not stats.empty:
                if not stats[stats['date'] == selected_date].empty:
                    title = f'Dengue Cases and Deaths on {pd.to_datetime(selected_date).strftime("%B %d, %Y")}' + (f' in {selected_location}' if selected_location else '') + (f' in {selected_region}' if selected_region else '')
                    chart_html = create_chart_x_date(stats, title, selected_date)
                    has_data = True
                else:
                    title = f'No data available for {pd.to_datetime(selected_date).strftime("%B %d, %Y")}' + (f' in {selected_location}' if selected_location else '') + (f' in {selected_region}' if selected_region else '')
                    chart_html = create_chart_x_date(stats, title, selected_date)
                    has_data = False
            else:
                chart_html = ''
        elif selected_region:
            stats = df_filtered.groupby('loc').agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()

            if not stats.empty:
                # Find the location with the maximum total cases and deaths across all locations within the selected region
                max_cases_location = stats.loc[stats['cases'].idxmax(), 'loc'] if stats['cases'].max() > 0 else ''
                max_deaths_location = stats.loc[stats['deaths'].idxmax(), 'loc'] if stats['deaths'].max() > 0 else ''

                title = f'Dengue Cases and Deaths' + (f' in the month of {selected_month}' if selected_month else '') + (f' in {selected_region}' if selected_region else '') + f' Over the Years'
                chart_html = create_chart_x_location(stats, title) if not stats.empty else ''
        else:
            stats = df_filtered.groupby('year').agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()
            max_cases_month = None
            max_deaths_month = None
            max_cases_date = None
            max_deaths_date = None
            max_cases_location = None
            max_deaths_location = None
            has_data = None
            title = f'Dengue Cases and Deaths' + (f' in the month of {selected_month}' if selected_month else '') + (f' in {selected_location}' if selected_location else '') + f' Over the Years'
            chart_html = create_chart_overall_stats(stats, title) if not stats.empty else ''

        # checking the value of the stats for generating narration
        if not stats.empty:
            if selected_date:
                max_deaths_date = None
                max_cases_date = None
                max_cases_month = None
                max_deaths_month = None
                max_cases_year = None
                max_deaths_year = None
                max_cases_location = None
                max_deaths_location = None
            elif selected_region:
                max_deaths_date = None
                max_cases_date = None
                max_cases_month = None
                max_deaths_month = None
                max_cases_year = None
                max_deaths_year = None
                has_data = None
            else:
                max_cases_year = int(stats.loc[stats['cases'].idxmax()]['year']) if stats['cases'].max() > 0 else ''
                max_deaths_year = int(stats.loc[stats['deaths'].idxmax()]['year']) if stats['deaths'].max() > 0 else ''
        else:
            max_cases_location = None
            max_deaths_location = None
            max_cases_year = None
            max_deaths_year = None
            has_data = None

        narration = generate_narration(max_cases_year, max_deaths_year, max_cases_month, max_deaths_month, max_cases_date, max_deaths_date, max_cases_location, max_deaths_location, selected_location, selected_month, selected_year, selected_date, selected_region, has_data) if not stats.empty else f"<b>No data available for the selected filters.</b>"

    # if selected_date:
    #     selected_date_formatted = selected_date.strftime('%Y/%m/%d')
    # else:
    #     selected_date_formatted = None

    context = {
        'dengue_data': df.head(5).to_dict(orient='records'),
        'chart_html': chart_html,
        'narration': narration,
        'unique_years': unique_years,
        'unique_months': unique_months,
        'locations': locations,
        'regions': regions,
        'selected_location': selected_location,
        'selected_region': selected_region,
        'selected_month': selected_month,
        'selected_year': int(selected_year) if selected_year else None,
        'selected_date': selected_date,
    }

    return render(request, 'visualize/project1.html', context)

# Mapping
def project2(request):
    return render(request, 'visualize/project2.html')


# Bonus
def project3(request):
    return render(request, 'visualize/project3.html')

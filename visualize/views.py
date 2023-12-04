from django.shortcuts import render, redirect

# added
import json
from django.http import HttpResponse
import pandas as pd
import numpy as np
from .models import Dengue, FamilyIncomeExpenditure
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

# year
# all input fields
# quick: highest total number of cases (location)
# quick: highest total number of deaths (location)
# quick: highest total number of cases (specific date)
# quick: highest total number of deaths (specific date)

def clean_data(df):
    df = df.dropna(subset=['loc'])
    df['loc'] = df['loc'].replace('SISQUIJOR', 'SIQUIJOR')
    df['cases'] = df['cases'].fillna(0)
    df['deaths'] = df['deaths'].fillna(0)
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
    df['year'] = pd.to_datetime(df['date'], errors='coerce').dt.year
    df['month'] = pd.to_datetime(df['date'], errors='coerce').dt.month
    return df

def generate_narration(max_cases_year, max_deaths_year, selected_location, selected_month):
    narration = f"The graph illustrates Dengue cases and deaths"

    if selected_month:
        narration += f" in the month of {selected_month}"

    if selected_location:
        narration += f" in {selected_location}"

    narration += " across years.<br><br>"

    if max_cases_year != 0:
        narration += f"The year with the highest total number of cases is {max_cases_year}.<br><br>"

    if max_deaths_year != 0:
        narration += f"The year with the highest total number of deaths is {max_deaths_year}.<br><br>"

    return narration

def create_chart(location_stats, title, height=500):
    fig = px.line(location_stats, x='year', y=['cases', 'deaths'], labels={'year': 'Year', 'value': 'Count'},
                  title=title, markers=True)
    fig.update_xaxes(tickmode='array', tickvals=location_stats['year'].unique())
    fig.update_layout(xaxis_title='Year', yaxis_title='Count', legend_title='Legend', height=height)
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

    if selected_location and selected_month:
        df_filtered = df[(df['loc'] == selected_location) & (df['month'] == unique_months.index(selected_month) + 1)]
    elif selected_month:
        df_filtered = df[df['month'] == unique_months.index(selected_month) + 1]
    elif selected_location:
        df_filtered = df[df['loc'] == selected_location]
    else:
        df_filtered = df

    location_stats = df_filtered.groupby('year').agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()
    max_cases_year = int(location_stats.loc[location_stats['cases'].idxmax()]['year'])
    max_deaths_year = int(location_stats.loc[location_stats['deaths'].idxmax()]['year'])

    narration = generate_narration(max_cases_year, max_deaths_year, selected_location, selected_month)
    title = f'Dengue Cases and Deaths in {selected_location} Over the Years' if selected_location else f'Dengue Cases and Deaths in the month of {selected_month} Over the Years' if selected_month else 'Dengue Cases and Deaths Over the Years'
    chart_html = create_chart(location_stats, title)

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


# Bonus Project
def clean_family_data(df):
    df['region'] = df['region'].replace('IX - Zasmboanga Peninsula', 'IX - Zamboanga Peninsula')
    df['region'] = df['region'].replace('XI - Davao Region', 'XI - Davao')
    df['region'] = df['region'].replace('Caraga', 'XIII - Caraga')
    
    return df

def bar_chart(chart_input, x_axis, title):
    fig = px.bar(chart_input, x=x_axis, y='region', color=x_axis, title=title, height=500)

    if x_axis == 'income':
        fig.update_layout(xaxis_title='Total Household Income', yaxis_title='Region', legend_title='Legend', height=500)
    else:
        fig.update_layout(xaxis_title=f'{x_axis.capitalize()} Expenditure', yaxis_title='Region')
    
    return fig.to_html()

def narrate_data(selected_region, selected_expenditure, region_expenditure_data):
    narration = f"The graph illustrates the total"

    if selected_expenditure == 'income':
        narration += f" <u>household income</u> of each region. "
    else:
        narration += f" <u>{selected_expenditure}</u> expenditure of each region. "
        
    narration += f"<br><br>"

    if selected_region:    
        narration += f"The region of <u>{selected_region}</u> tallied an appoximate value of <strong>{region_expenditure_data}</strong>."
    
    return narration


def project3(request):
    family_data = FamilyIncomeExpenditure.objects.all()
    df = pd.DataFrame(list(family_data.values()))
    df = clean_family_data(df)
    
    expenditure_columns = df.columns[3:].tolist()
    regions = sorted(df['region'].unique())

    display_names = {
        'food': 'Food Expenditure',
        'rice': 'Rice Expenditure',
        'bread_cereal': 'Bread and Cereals Expenditure',
        'meat': 'Meat Expenditure',
        'fish': 'Fish & Marine Products Expenditure',
        'fruits': 'Fruits Expenditure',
        'vegetables': 'Vegetables Expenditure',
        'hotels': 'Hotels and Restaurants Expenditure',
        'alcohol': 'Alcoholic Beverages Expenditure',
        'tobacco': 'Tobacco Expenditure',
        'clothing': 'Clothing, Footwear and Other Wear Expenditure',
        'housing': 'Housing and Water Expenditure',
        'medical': 'Medical Care Expenditure',
        'transport': 'Transportation Expenditure',
        'communication': 'Communication Expenditure',
        'education': 'Education Expenditure',
        'miscellaneous': 'Miscellaneous Goods and Services Expenditure',
        'occasions': 'Special Occasions Expenditure',
        'farming': 'Crop Farming and Gardening Expenditure',
    }
    expenditure_columns = [display_names.get(expenditure, expenditure) for expenditure in expenditure_columns]

    selected_expenditure = request.POST.get('expenditure')
    selected_region = request.POST.get('region')

    if selected_expenditure:
        selected_expenditure = [key for key, value in display_names.items() if value == selected_expenditure][0]
        agg_df = df.groupby('region').agg({selected_expenditure: 'sum'}).reset_index()
    else:
        agg_df = df.groupby('region').agg({'income': 'sum'}).reset_index()
        selected_expenditure = 'income'
    
    agg_df = agg_df.sort_values('region', ascending=False)

    region_expenditure_data = agg_df.loc[agg_df['region'] == selected_region, selected_expenditure].sum()

    narration = narrate_data(selected_region, selected_expenditure, region_expenditure_data)

    title = f'Total Household Income of Each Region' if selected_expenditure == 'income' else f'Total {selected_expenditure.capitalize()} Expenditure of Each Region'
    chart = bar_chart(agg_df, selected_expenditure, title)

    context = {
        'chart': chart,
        'narration': narration,
        'selected_expenditure': selected_expenditure,
        'expenditure_columns': expenditure_columns,
        'regions': regions,
        'selected_region': selected_region
    }

    return render(request, 'visualize/project3.html', context)

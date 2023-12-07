# Project 1

### Setting up project

1. **Create a Folder:**
   - Create a new folder. This folder serves as the central location for your Django project and app. (Like a main folder).

2. **Navigate to the Folder:**
   - Open your terminal or command prompt and navigate to the created folder.
     ```bash
     cd your_project_folder
     ```

3. **Activate Virtual Environment:**
   - Create and activate a virtual environment using Pipenv.
     ```bash
     pipenv shell
     ```

4. **Install Django:**
   - Install Django using Pipenv.
     ```bash
     pipenv install django
     ```

5. **Start Django Project:**
   - Use Django's admin tool to start a new project.
     ```bash
     django-admin startproject your_project_name
     ```

6. **Navigate to Project Folder:**
   - Move into the project folder.
     ```bash
     cd your_project_name
     ```

7. **Check for 'manage.py':**
   - Ensure that the 'manage.py' file is present in the project folder.

8. **Create a Django App:**
   - Create a new Django app within the project.
     ```bash
     python manage.py startapp your_app_name
     ```

9. **Install Dependencies:**
   - Move the 'Pipfile' and 'Pipfile.lock' from the initial folder to the Django project folder.
     ```bash
     cd your_project_name
     pipenv install
     ```

10. **Update and Sync Dependencies:**
    - Update and sync dependencies for the project.
      ```bash
      pipenv update
      pipenv sync
      ```

11. **Install Additional Dependencies:**
    - It's okay to install other dependencies during development. Install them in the folder where 'manage.py', 'Pipfile', and 'Pipfile.lock' are located and inside the Django project.
      ```bash
      pipenv shell
      pipenv install django
      pipenv install djangorestframework django-cors-headers
      pipenv install pandas
      pipenv install statsmodels
      pipenv install scikit-learn
      pipenv install numpy
      ```

12. **Install PostgreSQL (if needed):**
    - If using PostgreSQL, install the required package.
      ```bash
      pipenv install psycopg2==2.7.7
      ```

13. **Configure PostgreSQL:**
    - In pgAdmin, create a database with appropriate settings.

14. **Update Database Settings:**
    - Back in the project, update the database name and password in your 'settings.py'.



## Import CSV to PostgreSQL Using Django Management Commands

### Preparing and Importing Data

1. **Create a Data Folder:**
   - In your main folder, create a folder to store your datasets.

2. **Check CSV Columns:**
   - Examine the columns of your CSV file to ensure compatibility with your Django model.

3. **Create Django Model:**
   - In the 'models.py' file of your Django app, define a model reflecting the CSV structure. Apply appropriate data types to each column.

4. **Management Commands Setup:**
   - Inside your Django app, create a 'management' folder. Within 'management', create a 'commands' folder.

5. **Create Command Files:**
   - In the 'commands' folder, create a file for each dataset. Write the code to import the CSV into the corresponding Django model.

6. **Run Migrations:**
   - Open the terminal and run migrations to apply the changes to your database.
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

7. **Run Import Commands:**
   - Execute commands to import CSV data into the database.
     ```bash
     python manage.py (name_of_the_file_to_import)
     ```

8. **Check Results in pgAdmin:**
   - Once the import process is successful, check the results in pgAdmin to ensure the data has been added to the respective tables.


## Development and Coding

### Running the Django Server

1. **Check Django Installation:**
   - Ensure Django is installed in your virtual environment.

2. **Run the Server:**
   - Start the Django development server to check if everything is working.
     ```bash
     python manage.py runserver
     ```

### Adding Your Django App to Settings

3. **Modify 'settings.py':**
   - Include your Django app in the 'INSTALLED_APPS' section of 'settings.py'.
     ```python
     INSTALLED_APPS = [
         # other apps
         'your_app',
     ]
     ```

### Creating Django Templates

4. **Create Templates and Static Folders:**
   - Organize your HTML files in a 'templates' folder and store static files (CSS, JS, images) in a 'static' folder.
   
5. **Configure Templates in 'settings.py' (Django project folder):**
   - Connect your Django templates by configuring the 'TEMPLATES' section in 'settings.py'.
     ```python
     'DIRS': [os.path.join(BASE_DIR, 'templates')],
     ```

### Adding Routes

6. **Configure 'urls.py' (Django project folder):**
   - Open the 'urls.py' file in your Django project and connect your app's URLs.
     ```python
     from django.urls import path, include
     urlpatterns = [
         path('admin/', admin.site.urls),
         path('', include('your_app.urls')),
     ]
     ```

### Creating Views and Rendering HTML Pages

7. **Create HTML Templates:**
   - In the 'templates' folder, create 'base.html' (parent) and 'index.html' (child) files. 'base.html' can contain frontend dependencies or CDNs.

8. **Define Views in 'views.py':**
   - Create a view function in 'views.py' and render HTML pages.
   - Django views are responsible for handling the logic of your application, processing data, and deciding which template to render or which response to send back.
     ```python
     def index(request):
         # add logic here as needed for your views functionality
         return render(request, 'your_app/index.html')
     ```

9. **Configure URLs in 'urls.py' (Django app folder):**
   - Connect your app's views in 'urls.py'.
     ```python
     from django.urls import path
     from . import views

     urlpatterns = [
         path('', views.index, name="index"),
         # add more views here
     ]
     ```

10. **Check Browser:**
    - Visit your browser to ensure everything is working correctly.

**Note:**
Follow these steps vice versa to create additional views, templates, and static files for your Django project. Additionally, remember to:
1. Add a Django view to render an HTML page (`views.py`).
2. Include the route for the Django view in the project's URL configuration (`urls.py`). Add logic in your views as needed for functionality.
3. Repeat the process as necessary to enhance the functionality of your project.


## Data Visualization Development Steps

1. **Import Required Libraries:**
   - Ensure the necessary libraries are imported in your `views.py` file (or you can install other packages):

2. **Define Data Visualization Functions:**
   - Copy the provided functions into your `views.py` file. These functions handle data preprocessing, narration generation, and chart creation.
   - Data Prepocessing function
   ```python
     def clean_data(df):
       # Dropping missing values
       # Replacing certain location names
       # Filling NaN values in 'cases' and 'deaths' columns
       # Converting date columns to datetime format.
       return df
     ```
   - Function that handles user input.
   ```python
     def function_name(request):
       #add logic here
       context = {
        # add context dictionary you want to display in your templates
        # generate content in your web pages based on the data you pass from the server (views) to the client (templates).
    }

    return render(request, 'visualize/project1.html', context)
     ```

4. **Update Existing Views:**
   - Integrate the new data visualization logic into your existing views, such as `index` and `project1`. Handle user inputs appropriately.
     ```python
     def function_name(request):
      # Fetch all Dengue objects from the database using the Django ORM
      # Convert the Django QuerySet to a Pandas DataFrame
      # Clean the data using the clean_data function
      # Values for the dropdowns (locations, regions, years, and months)

      # Get user input
      # Handle user input combinations
      # Handle user inputs. Filter dataframe before calculating stats(total cases and deaths)
      # Separate stats based on whether a specific request is selected. Generate chart based on stats
      # stats => filtered data frame with total cases and deaths

      # Checking the value of the stats for generating narration
      # Default chart. By regions
       context = {
        # add context dictionary you want to display in your templates
        # generate content in your web pages based on the data you pass from the server (views) to the client (templates).
    }
   return render(request, 'visualize/project1.html', context)
     ```

6. **Create HTML Templates:**
   - Ensure you have HTML templates (e.g., 'visualize/project1.html') for rendering the data visualization charts. Customize the templates based on your application's design.

   ```markdown
   ### Data Visualization Usage

   - Ensure you have the required dependencies installed.
   - Start your Django development server.
   - Visit the data visualization page in your web browser.
   - Explore the charts by selecting different filters and options.
   - Follow the provided narration for insights into the data.

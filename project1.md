# Project 1

### Setting up project

1. **Create a Folder:**
   - Create a new folder for your Django project.

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
   - Outside the Django app, create a folder to store your datasets.

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

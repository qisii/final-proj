# final-proj

### Installing

1. Open a terminal and navigate to the project directory.

2. Activate the virtual environment:

    ```bash
    pipenv shell
    ```

5. Update and sync dependencies:

    ```bash
    pipenv update
    pipenv sync
    ```

6. In pgAdmin, create a database with appropriate settings.

7. Back in the project, update the database name and password in your settings.py

8. Run migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

9. Import geoplot dataset (if applicable):

    ```bash
    python manage.py import_pizza_data
    ```

10. Run the development server:

    ```bash
    python manage.py runserver
    ```

11. Access the project at http://127.0.0.1:8000/.

## Troubleshooting

### Warning: Python 3.12 was not found on your system...

If you encounter this warning when running `pipenv shell`:

1. Check your current Python version:

    ```bash
    python --version
    ```

2. Update Python version:

    ```bash
    pipenv --python path/to/python
    ```

    Replace `path/to/python` with the path from step 1.

3. Activate the virtual environment:

    ```bash
    pipenv shell
    ```

4. Update and sync dependencies:

    ```bash
    pipenv update
    pipenv sync
    ```

5. Continue with the installation steps mentioned above.

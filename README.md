This repository represents a course project of University of Delaware CISC682 Introduction to Human-Computer Interaction.

To run the backend server, a MySQL database is needed. This project uses Python3 and PyMySQL library to connect to MySQL database.

To install Python3 and Pip3 on your operation system, please refer to document provided by [Python.org](https://www.python.org).

Then install PyMySQL library by Pip3:

    $ python3 -m pip install PyMySQL

Before running the backend server, database need to be initialized:

    $ python3 initialize_database.py

To insert random test data to the database:

    $ python3 insert_random_data.py

Then start backend server by:

    $ python3 web.py

By default, the website will be running on [http://127.0.0.1:5000/](http://127.0.0.1:5000/).
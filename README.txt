Prerequisites:
-Python 2.7
-PostgreSQL
-SQLAlchemy 0.8.4
-werkzeug 0.8.3
-flask 0.9
-Flask-Login 0.1.3


Quick start
-Install Vagrant and VirtualBox.
-Clone the fullstack-nanodegree-vm from following address:
	https://github.com/udacity/fullstack-nanodegree-vm
-Download the zip from:
	https://github.com/m-sepehrnoush/bookexchangeprogram
-Launch the vm with "vagrant up" command.
-Connect to the vm with "vagrant ssh" command.
-"CD" to "bep" folder.
-Run "project.py" with the following command:
 "python project.py".
-Navigate to 127.0.0.1:5000 on your web-browser
-The Webserver can be stopped with Ctrl+C on the Vagrant.


What's included:
-bookexchangeprogram/
 |--bep/
 |  |--static/
 |	|	|--bg.png
 |	|	|--blank_user.gif
 |	|	|--styles.css
 |	|	|--top-banner.jpg
 |  |--templates/
 |	|	|--book.html
 |	|	|--deletebook.html
 |	|	|--deletegenre.html
 |	|	|--editbook.html
 |	|	|--editgenre.html
 |	|	|--genres.html
 |	|	|--header.html
 |	|	|--login.html
 |	|	|--main.html
 |	|	|--newbook.html
 |	|	|--newgenre.html
 |	|	|--publicbook.html
 |	|	|--publicgenres.html
 |  |--client_secrets.json
 |  |--database_setup.py
 |  |--database_setup.pyc
 |  |--library.db
 |  |--lotsofbooks.py
 |  |--project.py
 |--README.txt


Notes:
This is an Item Catalog application for Udacity's FSND P3.
You can create an empty database named 'library.db' using the command:
 "python database-setup.py"
You can populate 'library.db' using dummy data using the command:
 "python lotsofbooks.py"

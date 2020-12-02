# Short url

A basic url shortener

### Prerequisites

You need to have python3 and virtualenv installed.
```
$ sudo apt update
$ sudo apt install -y python3-pip
$ sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
$ sudo apt install -y python3-venv
```

### Installing

Clone this repository.
```
$ cd ~
$ git clone git@github.com:Katalam/short_url.git
$ cd short_url
```
Now we need to setup the virtual environment.
```
$ python -m venv venv
```
To be safe all packages getting installed correctly we will install wheel
```
$ pip install wheel
```
Now activate thee virtual environment and install the dependencies.
```
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```
We need to have a mysql database and in order get one.
```
(venv) $ sudo apt install mysql-server
(venv) $ sudo mysql_secure_installation
```
```
Securing the MySQL server deployment.

Connecting to MySQL using a blank password.

VALIDATE PASSWORD COMPONENT can be used to test passwords
and improve security. It checks the strength of password
and allows the users to set only those passwords which are
secure enough. Would you like to setup VALIDATE PASSWORD component?

Press y|Y for Yes, any other key for No: Y

There are three levels of password validation policy:

LOW    Length >= 8
MEDIUM Length >= 8, numeric, mixed case, and special characters
STRONG Length >= 8, numeric, mixed case, special characters and dictionary file

Please enter 0 = LOW, 1 = MEDIUM and 2 = STRONG:
2
```
Set a secure rememberable password.
```
Please set the password for root here.


New password:

Re-enter new password:
```
```
Estimated strength of the password: 100
Do you wish to continue with the password provided?(Press y|Y for Yes, any other key for No) : Y
```
Now we change the authentification for the mysql root account to password instead of the auth-socket.
```
sudo mysql
```
Following with your rememberable secure password.
```
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'password';
mysql> FLUSH PRIVILEGES;
mysql> exit
```
You are now able to relog with your choosen password to create a new user or you use the root account. To check the status of the mysql service.
```
$ systemctl status mysql.service
```
If the the output is like
```
● mysql.service - MySQL Community Server
     Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2020-04-21 12:56:48 UTC; 6min ago
   Main PID: 10382 (mysqld)
     Status: "Server is operational"
      Tasks: 39 (limit: 1137)
     Memory: 370.0M
     CGroup: /system.slice/mysql.service
             └─10382 /usr/sbin/mysqld
```
everything if fine and you can continue.
Back to your project folder.
```
(venv) $ cp .env.example .env
(venv) $ vim .env
```
And there you change your mysql user and password. You also need to change the base url in order to create the copy ready link for the user.


### Running the test
Run
```
(venv) $ python url.py
```
if output is like
```
 * Serving Flask app "url" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
everything is fine and the server is running.

## Deployment
A good tutorial to serve the app on Ubuntu can be found [here](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04).

## Built with

* Flask
* MySQL

## Author

* [Katalam](https://github.com/Katalam)

## License

This project is licensed under the GPLv3 License - see [LICENSE](LICENSE) file for details.

#100ProjectsOfCode

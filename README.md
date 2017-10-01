### Install global dependencies
 * [Python 3.6.2](https://www.python.org/downloads/)
 * [MySQL](https://www.mysql.com/downloads/)
 * Virtualenv
   * Linux: ```sudo pip install virtualenv```
   * MacOS: ```sudo brew install virtualenv```
### Clone
```sh
mkdir ~/projects
cd ~/projects
git clone git@github.com:teimurjan/discount-code-store.git
cd discount-code-store
```
### Install local dependencies
```sh
virtualenv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt
```
### Configure db
```sh
mysql -u<your_username> -p<your_password>
create database store;
exit;
./manage.py migrate
```
### Start
 * Create super user
 ```sh 
 ./manage.py createsuperuser
 ```
 * Run
 ```sh
 ./manage.py runserver
 ```
### Additional info
 * You should use your own MySQL username and password which should
replace the initial ones in the main/settings.py.
 * Codes can be given out by users with staff and admin statuses.
# BookQuest

This engaging web app invites book lovers to test their literary knowledge through fun quizzes featuring famous quotes. Users can select from various quiz lengths, challenging themselves to guess which book a particular quote is from.

In addition to taking quizzes, users have the opportunity to create and submit their own book quotes, enriching the community with personal favorites. The app features a scoreboard that tracks users' progress and performance, fostering friendly competition

Users can create an account to monitor their quiz results and achievements over time or opt to participate as a guest for a quick and casual experience.

## Installation

1. **Clone the repository:**
```
git clone https://github.com/jthomas981/BookQuest/
cd BookQuest
```

2. **Set up a virtual environment:**
If you don’t have virtualenv installed, you can install it via pip:
```
pip install virtualenv
```
Then create and activate a virtual environment:
* For macOS/Linux:
```
virtualenv venv
source venv/bin/activate
```
* For Windows:
```
python -m venv venv
venv\Scripts\activate
```

3. **Create the `.env` file:**
In the root directory, create a `.env` file and add the necessary environment variables. See the example `.env.example` file for how the `.env` is supposed to look like.

4. **Install dependencies using the provided script:**
* For macOS/Linux:
```
./build.sh
```
* For Windows:
```
build.bat
```

This script will:
* Install the necessary Python packages listed in requirements.txt.
* Collect static files for your app.
* Apply any outstanding database migrations.

## Usage 

After running the build script, you can start your application using:
```python manage.py runserver```
Access the app at http://127.0.0.1:8000.

# THE BLOG SLUG

A website for established and aspiring bloggers/journalists to publish their articles, catch up on the latest headlines, and interact with people of interest by following, messaging, and commenting.

## Features

- User authentication

- OTP verification for signup and password recovery

- User details update

- User following

- User messaging

- Chat archiving

- News updates from user's country

- Blog posting

- Bookmarking and commenting on posts

- Deletion of comment and posts by owners

- Responsive design for desktop and mobile


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`

`DEBUG`

`EMAIL_HOST`

`EMAIL_HOST_USER`

`EMAIL_HOST_PASSWORD`

`DEFAULT_FROM_EMAIL`

`WORLD_NEWS_API_KEY`

`NEWS_REFRESH_INTERVAL`


## Installation

- Open a terminal and clone this repo to your desired folder

- Run `"pip install -r requirements.txt"`

- Create your .env file and set the necessary environment variables

- Inside the project folder, run "python manage.py makemigrations" followed by "python manage.py migrate" to initialize your database

- Lastly, run...

```bash
  python manage.py runserver
```

## Tests


Before carrying out tests, set DEBUG to True in your .env file, open the trendcatcher.py file inside the core app and unhash the "if" code block from line 22 to line 25.

This will eliminate the need for an api key to use the worldnewsapi, and you will be served a static json file containing news articles to be displayed on the homepage.

To use worldnewsapi to get realtime news, signup, and add your api key (WORLD_NEWS_API_KEY) variable to your .env and connect to the internet.

## Authors

- [Github@victorsunny](https://www.github.com/victorsunny/)

- [LinkedIn@victorsunny](https://www.linkedin.com/in/victor-sunny-6b06ba220)

## 🚀 About Me
Hello there, Victor here.

I am a backend developer, and i believe every problem that can be fixed, will be fixed if given enough effort, dedication, and critical thinking, skills all of which are in my possession.

I am highly proficient in backend web/app developement using Python and it's related technologies, readily adopting and adapting to new, required technologies, meeting up to industry standards, quality, and reliability.


## Tech Stack

**Client:** HTML, TailwindCSS

**Server:** Python, Django, Django rest framework, Sqlite, Whitenoise.


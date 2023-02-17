# Blog Static Site Generator



## About The App
This is a simple static site generator. 
It takes a folder `content` that contain markdown files for the  different pages for the site and produces html files for these pages.
The markdown files inclide pages for the different articles and for support pages such as about page and error page.



## Technologies
I used `Python`, `Jinja2`, `markdown`, `toml`



## Setup locally
- download or clone the repository
- activate the virtual environment using the command `pipenv shell`

If pipenv is not installed in your machine, you can install it using the command `pip3 install pipenv`

- run the app using the command `python3 main.py`
- Run the development server:
    - cd into public
    - run `python3 -m http.server`


## References
[Build a simpla static site generator](https://www.youtube.com/watch?v=Ph7oJDR71Jc)
[Create a static site generator with Python](https://docs.replit.com/tutorials/python/static-site-generator)
[Toml documentation](https://toml.io/en/)
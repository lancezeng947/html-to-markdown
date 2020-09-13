# html-to-markdown
Welcome to H2M, a webapp built using Python's Django framework for transforming your Kindle HTML exports into elegant Markdown format.

Please visit https://h2markdown.herokuapp.com/ to use our service. *Please allow some time for the page to load as it is running on a free Heroku server.*

## Project Summary:
*Problem:* Kindle Notebook Exports are an unattractive presentation of personal notes.   

*Solution:* Develop RPA solution to simplify conversion of standardized HTML template to Markdown 

*Technology Stack:* Python, Python Django, HTML, CSS, deployed using Heroku


## File Dictionary:
1. converter: Django application including `templates` HTML , `static` CSS, and webapp routing. The business logic, leveraging Python's `BeautifulSoup` to parse HTML is located in `script.py`

2. html_to_markdown: Django's management/settings 

3. registration: Experimental (WIP) application to allow user registration/login to save history of converted notebooks


## Notes:
The application **DOES NOT** save any uploaded data. 

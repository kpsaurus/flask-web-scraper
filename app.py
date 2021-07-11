from flask import Flask, request
from flask import render_template
from scraper import ScrapCovid, ScrapFootball
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    """
    For loading the home page.
    """
    return render_template('index.html')


@app.route('/covid')
def covid():
    """
    For loading the COVID-19 Statistics page.
    """
    # Getting the table data after scraping.
    table_h, table_b = ScrapCovid().get_table_data()

    # Data to be passed to the template.
    data = {'heading': table_h, 'body': table_b}

    # Returning the template.
    return render_template('covid.html', data=data)


@app.route('/football')
def football():
    """
    For loading the European Football League Standings page.
    """
    # Getting the league and year from the GET request.
    league = request.args.get('league')
    year = request.args.get('year')

    # Current year.
    current_year = datetime.today().year

    if year is None:
        # No year is provided.
        # Default value of the year would be current year.
        year = current_year

    seasons = []
    # Populating a list of last 3 season details.
    for i in range(3):
        season_year = current_year - 1 - i
        season_full = f'{season_year}-{season_year - 1999}'
        season = {'year': season_year, 'season': season_full}
        seasons.append(season)

    available_leagues = ['premier-league', 'la-liga', 'bundes-liga', 'ligue-1']

    available_leagues_names = {'premier-league': 'Premier League',
                               'la-liga': 'Laliga',
                               'bundes-liga': 'Bundesliga',
                               'ligue-1': 'Ligue 1'
                               }

    if league in available_leagues:
        # Provided league is present in the available_leagues.
        table_h, table_b = ScrapFootball(league, year).get_table_data()
        data = {'heading': table_h, 'body': table_b, 'league': available_leagues_names.get(league), 'seasons': seasons}
    elif league is None:
        # Default league is the Premier League.
        table_h, table_b = ScrapFootball('premier-league', year).get_table_data()
        data = {'heading': table_h, 'body': table_b, 'league': available_leagues_names.get('premier-league'),
                'seasons': seasons}
    else:
        # Not a valid league.
        data = {'seasons': seasons}

    # Returning the template.
    return render_template('football.html', data=data)

from bs4 import BeautifulSoup
import requests

headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}


class ParseTable:
    """
    A class for parsing the scraped table data.
    """

    def __init__(self, table):
        """
        Constructor of the class.
        @param table: Scraped table.
        """
        table_heading = table.find('thead')
        self.table_heading_row = table_heading.find_all('tr')
        self.table_heading_data = []

        table_body = table.find('tbody')
        self.table_body_data = []
        self.table_body_rows = table_body.find_all('tr')

    def get_table_data(self):
        """
        Returns both table header data as well as body data.
        @return: Two lists viz - table_heading_data and
        table_body_data
        """
        # Looping through the table header cells and populating
        # the table_heading_data.
        for row in self.table_heading_row:
            columns = row.find_all('th')
            for column in columns:
                spans = column.find('span', attrs={'class': 'hide-for-small'})
                if spans is None:
                    self.table_heading_data.append(column.text.strip())
                else:
                    self.table_heading_data.append(spans.text.strip())

        # Looping through the table body cells and populating
        # the table_body_data.
        for row in self.table_body_rows:
            columns = row.find_all('td')
            columns = [column.text.strip() for column in columns]
            self.table_body_data.append([column for column in columns if column])

        return self.table_heading_data, self.table_body_data


class ScrapFootball(ParseTable):
    """
    For scraping the transfermarkt.com
    """

    def __init__(self, league=None, year=None):
        """
        Constructor of the class.
        @param league: A domestic league - for eg: premier-league.
        @param year: Year in YYYY format.
        """

        # League URLs based on the provided league.
        if league == 'premier-league' and year is not None:
            self.leage_table_url = f'https://www.transfermarkt.com/premier-league/tabelle/wettbewerb/GB1/saison_id/{year}'
        elif league == 'la-liga' and year is not None:
            self.leage_table_url = f'https://www.transfermarkt.com/laliga/tabelle/wettbewerb/ES1?saison_id={year}'
        elif league == 'bundes-liga' and year is not None:
            self.leage_table_url = f'https://www.transfermarkt.com/bundesliga/tabelle/wettbewerb/L1?saison_id={year}'
        elif league == 'ligue-1' and year is not None:
            self.leage_table_url = f'https://www.transfermarkt.com/ligue-1/tabelle/wettbewerb/FR1?saison_id={year}'

        # Scraping the web page.
        self.pageTree = requests.get(self.leage_table_url, headers=headers)
        self.soup = BeautifulSoup(self.pageTree.content, 'html.parser')
        # Getting the table div.
        self.league_table_div = self.soup.find('div', attrs={'class': 'responsive-table'})

        # Calling the parent's constructor and passing the argument.
        super().__init__(self.league_table_div)


class ScrapCovid(ParseTable):
    """
    For scraping the covidstatistics.org
    """

    def __init__(self):
        """
        Constructor of the class.
        """
        self.table_url = 'https://covidstatistics.org/'
        # Scraping the web page.
        self.pageTree = requests.get(self.table_url, headers=headers)
        self.soup = BeautifulSoup(self.pageTree.content, 'html.parser')
        # Getting the table.
        self.covid_table = self.soup.find('table', attrs={'id': 'data-info-table'})

        # Calling the parent's constructor and passing the argument.
        super().__init__(self.covid_table)

"""Wikipedia Software Robot

This module contains three classes:
1) WikiRobot
    An abstract super class capable of extracting information from Wikipedia.
    This class contains general functions for a software robot to navigate on Wikipedia. 
    Because Wikipedia has different content structures for different categories
    (for example Animals, Countries, or People), any function that requires knowledge
    about specific categories need to be implemented in a subclass.
2) WikiScientistRobot
    A subclass of WikiRobot, able to extract information about scientists from Wikipedia.
3) WikiScientist
    A helper class which holds information about scientists.
"""

import datetime
from abc import ABC, abstractmethod
from RPA.PDF import PDF
from RPA.Browser.Selenium import Selenium
from utils.dialog_builder import show_dialog
from utils.html_template import create_html_report


class WikiRobot(ABC):
    """
    An abstract class to extract information from Wikipedia.

    The class represents a software robot, i.e. it uses the RPA framework
    to search for Wikipedia articles, extracts information from the article,
    and creates a report with all findings. This super class implements all
    necessary methods to handle navigation on Wikipedia. However, Wikipedia
    has different content structures for different categories (e.g. Animals,
    Countries, or People). That is why subclasses have to be implemented
    to handle 1) extraction of information and 2) creation of the report. 

    Attributes
    ----------
    name : str
        the name of the software robot
    url : str
        the url of the Wikipedia instance
    data : list
        holds all extracted information
    br : RPA.Browser.Selenium.Selenium
        a browser instance of Selenium

    Methods
    -------
    run(articles, output_path)
        Starts the software robot for a given list of articles
    instructions(articles)
        Presents the software robot's instructions to the user
    report(output_path)
        Creates a report containing all extracted information
    get_content(article)
        Retrieves information from an article
    search_article(article)
        Navigates to an article
    get_location()
        Returns the current URL
    get_title()
        Returns the title of the current webpage
    get_domain(url)
        Returns the base domain name of a given URL
    is_at_article(article)
        Verifies if the browser is at the given article
    open_browser()
        Opens a new browser instance
    close_browser()
        Closes all browser instances
    is_browser_open()
        Verifies if a browser instance is open
    show_dialog_error()
        Displayes an error dialog
    
    Abstract Methods
    ----------------
    extract_from_article(article)
        Extracts certain information from an article
    create_report(output_path)
        Creates a report with all findings
    show_dialog_start(articles)
        Displays instructions in a dialog 
    show_dialog_completed(output_path)
        Displays a dialog when software robot is done
    """

    def __init__(self, name):
        """
        Parameters
        ----------
        name : str
            The name of the software robot
        """

        assert isinstance(name, str)
        self.name = name
        self.url = "https://www.wikipedia.org"
        self.data = []
        self.br = Selenium()

    def run(self, articles, output_path):
        """Starts the software robot and creates a report.

        For each `article`, the software robot searches the corresponding
        Wikipedia article, extracts relevant information, and creates a
        report. 

        Parameters
        ----------
        articles : list
            A list of articles, specified by strings
        output_path : str
            The path where the report is written to
        """

        assert isinstance(articles, list)
        assert len(articles) > 0
        assert all(isinstance(a, str) for a in articles)
        assert isinstance(output_path, str)

        self.instructions(articles)
        try:
            for article in articles:
                self.data.append(self.get_content(article))
        except:
            self.close_browser()
            self.show_dialog_error()
            return
        else:
            self.close_browser()
            self.report(output_path)
    
    def instructions(self, articles):
        """Displays a dialog containing instructions.

        Parameters
        ----------
        articles : list
            A list of articles, specified by strings
        """

        assert isinstance(articles, list)
        assert len(articles) > 0
        assert all(isinstance(a, str) for a in articles)

        self.show_dialog_start(articles)
    
    def report(self, output_path):
        """Creates a report and displays a final dialog.

        Parameters
        ----------
        output_path : str
            The path where the report is written to
        """

        assert isinstance(output_path, str)

        self.create_report(output_path)
        self.show_dialog_completed(output_path)

    def get_content(self, article):
        """Opens a browser, searches for an article, and extracts information.

        Parameters
        ----------
        article : str
            The name of the Wikipedia article
        
        Returns
        -------
        Object
            Extracted information
        
        Raises
        ------
        RuntimeError
            If the article could not be found
        """

        assert isinstance(article, str)

        if not self.is_browser_open():
            self.open_browser()
        self.search_article(article)
        if not self.is_at_article(article):
            raise RuntimeError("Could not find article")
        return self.extract_from_article(article)
    
    def search_article(self, article):
        """Navigates to Wikipedia, enteres the name of the article in
        the search input, and clicks the search button.

        Parameters
        ----------
        article : str
            The name of the Wikipedia article
        
        Raises
        ------
        ElementNotFound
            If search box or search button cannot be found
        """

        assert isinstance(article, str)

        self.br.go_to(self.url)
        self.br.input_text("id:searchInput", article)  # Search box
        self.br.click_button("id:search-form >> tag:button")  # Search botton
    
    def get_location(self):
        """Returns the URL of the current browser instance.

        Returns
        -------
        str
            The URL of the current browser instance
        
        Raises
        ------
        NoSuchWindowException
            If no browser is open
        """

        return self.br.get_location() 

    def get_title(self):
        """Returns the title of the current browser instance.

        Returns
        -------
        str
            The title of the current browser instance
        
        Raises
        ------
        NoSuchWindowException
            If no browser is open
        """

        return self.br.get_title()

    def get_domain(self, url):
        """Returns the base domain name of a given URL.

        For example, the base domain name of https://www.en.wikipedia.org/wiki/domain
        is 'wikipedia'.

        Parameters
        ----------
        url : str
            A URL
        
        Returns
        -------
        str
            The base domain name of `url`
        """

        assert isinstance(url, str)

        return url.split(".")[1].lower()
    
    def is_at_article(self, article):
        """Verifies if the browser is at the given article.

        The browser is at the given article, when 1) the current
        base domain name matches Wikipedia's base domain name, and
        2) the current title contains the name of the article.

        Parameters
        ----------
        article : str
            The name of the Wikipedia article
        
        Returns
        -------
        bool
            True, if browser is at the given article, False otherwise
        """

        assert isinstance(article, str)

        if self.get_domain(self.url) != self.get_domain(self.get_location()):
            return False
        if article.lower() not in self.get_title().lower():
            return False
        return True

    def open_browser(self):
        """Opens a new browser instance."""
        self.br.open_available_browser()

    def close_browser(self):
        """Closes all browser instances."""
        self.br.close_all_browsers()

    def is_browser_open(self):
        """Returns True if at least one browser instance is open."""
        return len(self.br.get_browser_ids()) > 0
    
    def show_dialog_error(self):
        """Displays an error message in a dialog."""
        title = self.name
        header = "Something went wrong"
        button = "Okay"
        body = ["Unfortunately, the software robot encountered an issue.",
                "Please try again or contact support."]
        show_dialog(body=body, title=title, header=header, button=button)

    @abstractmethod
    def extract_from_article(self, article):
        """Extracts certain information from an article."""
        pass

    @abstractmethod
    def create_report(self, output_path):
        """Creates a report with all findings."""
        pass

    @abstractmethod
    def show_dialog_start(self, articles):
        """Displays instructions in a dialog."""
        pass

    @abstractmethod
    def show_dialog_completed(self, output_path):
        """Displays a dialog for when software robot is done."""
        pass


class WikiScientistRobot(WikiRobot):
    def __init__(self, name):
        """
        Parameters
        ----------
        name : str
            The name of the software robot
        """

        super().__init__(name)
    
    def extract_from_article(self, name):
        """Extracts date of birth, date of death, and the first paragraph
        from the current browser instance.

        Note: the method assumes that a browser is open and located at
        the requested article.

        Parameters
        ----------
        name : str
            The name of the scientist (and article)

        Returns
        -------
        WikiScientist
            A new object holding all extracted information
        
        Raises
        ------
        ElementNotFound
            If either date of birth, date of death, or first paragraph
            cannot be found
        """

        assert isinstance(name, str)

        date_of_birth = self._get_date_of_birth()
        date_of_death = self._get_date_of_death()
        first_paragraph = self._get_first_paragraph()
        return WikiScientist(name, date_of_birth, date_of_death, first_paragraph)

    def create_report(self, output_path):
        """Creates a PDF report with all findings.

        The PDF report has a title, preparation date,
        information of all found scientists. 

        Parameters
        ----------
        output_path : str
            The path where the report is written to
        """

        assert isinstance(output_path, str)

        pdf = PDF()
        date = datetime.datetime.now().date().strftime("%b %d, %Y")  # Today's date
        content = create_html_report(self.data, date)  # Uses HTML template
        pdf.html_to_pdf(content, output_path)

    def _get_date_of_birth(self):
        """Returns the date of birth."""
        return self._get_biography_date("Born")
    
    def _get_date_of_death(self):
        """Returns the date of death."""
        return self._get_biography_date("Died")
    
    def _get_first_paragraph(self):
        """Returns the first paragraph of the current Wikipedia article.

        Note: the method assumes that a browser is open and located at
        the requested article.

        Returns
        -------
        str
            The first paragraph of the current Wikipedia article
        
        Raises
        ------
        ElementNotFound
            If the first paragraph cannot be found
        """
        # The xpath points to the first paragraph `p` with:
        # 1) parent is `div` with id `bodyContent`
        # 2) paragraph does not have class `mw-empty-elt`
        xpath = ('xpath://div[@id="bodyContent"]' +
                 '//p[not(contains(@class, "mw-empty-elt"))]')
        return self.br.get_text(xpath)
    
    def _biography_lookup(self, header):
        """Returns the xpath to the table cell with given `header`.

        Returns
        -------
        str
            The xpath to the requested table cell
        """

        assert isinstance(header, str)

        return ('xpath://table[@class="infobox biography vcard"]' + # Find biography table
                f'//th[contains(text(), "{header}")]' +             # Look for given table header (th) 
                '//../td/span')                                     # Move to its table data (td)
    
    def _get_biography_date(self, header):
        """Returns a date located in the biography table.

        Note: the method assumes that a browser is open and located at
        the requested article.

        Parameters
        ----------
        header : str
            A table header of the biography table

        Returns
        -------
        datetime.date
            The requested date
        
        Raises
        ------
        ElementNotFound
            If the date cannot be found
        """

        assert isinstance(header, str)

        xpath = self._biography_lookup(header) # For example, xpath pointing to date of birth
        date = self.br.get_element_attribute(xpath, "textContent") # Get date from page
        # Removes parenthesis if present
        if date.startswith("("):
            date = date[1:]
        if date.endswith(")"):
            date = date[:-1]
        return datetime.datetime.strptime(date, "%Y-%m-%d").date()
    
    def show_dialog_start(self, articles):
        """Displays instructions in a dialog.

        This dialog is displayed before the software robot opens a browser.

        Parameters
        ----------
        articles : list
            A list of articles, specified by strings
        """

        assert isinstance(articles, list)
        assert len(articles) > 0
        assert all(isinstance(a, str) for a in articles)

        title = self.name
        header = self.name
        button = "Start"
        body = ["Hi! I'm the Wiki-Scientist-Robot. I'm here to help you save time " +
                "by extracting information about famous scientists from Wikipedia.",
                "These are the steps I'm going to take:",
                "1. Navigate to Wikipedia\n" +
                "2. Search for a scientist\n" +
                "3. Extract the following information: date of birth, date of death, " +
                    "age, and the first paragraph of their article\n" +
                "4. Create a PDF report with all findings",
                "These are the scientists I'm going to search today: " + ", ".join(articles),
                "When you're ready, simply click the start button to begin."]
        show_dialog(body=body, title=title, header=header, button=button)

    def show_dialog_completed(self, output_path):
        """Displays a dialog for when software robot is done.

        This dialog contains a link to the created PDF report.

        Parameters
        ----------
        output_path : str
            The path where the report was written to
        """

        assert isinstance(output_path, str)

        title = self.name
        header = self.name
        button = "Done"
        body = ["I'm already done!",
                "Below you can find a link to the report."]
        file = output_path
        show_dialog(body=body, title=title, header=header, file=file, button=button)


class WikiScientist:
    """
    A helper class that holds extracted information from scientists on Wikipedia.

    Attributes
    ----------
    name : str
        the name of the scientist
    date_of_birth : datetime.date
        the date of birth of the scientist
    date_of_death : datetime.date
        the date of death of the scientist
    summary : str
        the first paragraph of the article

    Methods
    -------
    get_age(date_of_birth, date_of_death)
        Returns the age of the scientist
    """

    def __init__(self, name, date_of_birth, date_of_death, summary):
        assert isinstance(name, str)
        assert isinstance(date_of_birth, datetime.date)
        assert isinstance(date_of_death, datetime.date)
        assert isinstance(summary, str)

        self.name = name
        self.date_of_birth = date_of_birth
        self.date_of_death = date_of_death
        self.summary = summary
        self.age = self.get_age(date_of_birth, date_of_death)
    
    def get_age(self, date_of_birth, date_of_death):
        """Calculates and returns the age given date of birth and death."""
        assert isinstance(date_of_birth, datetime.date)
        assert isinstance(date_of_death, datetime.date)

        age = date_of_death.year - date_of_birth.year
        # If birthday before date of death, substract one
        if (date_of_death.month < date_of_birth.month or
           (date_of_death.month == date_of_birth.month and
            date_of_death.day < date_of_birth.day)):
            age -=1
        return age

    def __eq__(self, other):
        """Equality operator, used for testing."""
        if not isinstance(other, WikiScientist):
            return False
        if self.name != other.name:
            return False
        if self.date_of_birth != other.date_of_birth:
            return False
        if self.date_of_death != other.date_of_death:
            return False
        if self.age != other.age:
            return False
        if self.summary != other.summary:
            return False
        return True

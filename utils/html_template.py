"""HTML Report Template

This module contains utility functions to create a report about
Wikipedia scientists in HTML. 
"""

import datetime


def create_html_report(scientists, date):
    """Returns an HTML report for the given scientists.

    Parameters
    ----------
    scientists : list
        A list of `WikiScientist` 
    date : datetime.date
        The date of when the report was prepared

    Returns
    -------
    str
        A HTML report for the given scientists
    """

    assert isinstance(scientists, list)
    assert len(scientists) > 0
    assert isinstance(date, str)

    header = html_header(date)
    sections = ''
    for scientist in scientists:
        sections += html_section(scientist.name,
                                 scientist.date_of_birth,
                                 scientist.date_of_death,
                                 scientist.age,
                                 scientist.summary)
    return html_document(header, sections)

def html_document(header, sections):
    """Fills in `header` and `sections` in an HTML template.

    Parameters
    ----------
    header : str
        The header part of the report, in HTML
    sections : str
        The sections part of the report, in HTML

    Returns
    -------
    str
        A report as HTML document
    """

    assert isinstance(header, str)
    assert isinstance(sections, str)

    return (f'<html>' +
            f'<head></head>' +
            f'<body>{header}{sections}</body>' +
            f'</html>')

def html_header(date):
    """Returns the header part of the report.

    The header contains a title (report name) and a subtitle (preparation date).

    Parameters
    ----------
    date : datetime.date
        The date of when the report was prepared

    Returns
    -------
    str
        The header part of the report, in HTML
    """

    assert isinstance(date, str)

    return (f'<h1 align="center">Wikipedia Scientist Report</h1>' +
            f'<h4 align="center">Prepared on {date}</h4>')

def html_section(name, date_of_birth, date_of_death, age, summary):
    """Returns a section of the report.

    Each scientist gets its own section containing extracted information.

    Parameters
    ----------
    name : str
        The name of the scientist
    date_of_birth : datetime.date
        The date of birth of the scientist
    date_of_death : datetime.date
        The date of death of the scientist
    summary : str
        The first paragraph of the article

    Returns
    -------
    str
        A section of the report, in HTML
    """
    assert isinstance(name, str)
    assert isinstance(date_of_birth, datetime.date)
    assert isinstance(date_of_death, datetime.date)
    assert isinstance(age, int)
    assert isinstance(summary, str)
    
    return (f'<br>' +
            f'<h3>{name}</h3>' +
            f'<ol><li><b>Date of Birth: </b>{date_of_birth}</li>' +
            f'<li><b>Date of Death: </b>{date_of_death}</li>' +
            f'<li><b>Age: </b>{age}</li>' +
            f'<li><b>Summary: </b>{summary}</li></ol>')

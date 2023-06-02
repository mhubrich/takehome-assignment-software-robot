"""Unit Tests

This module contains a number of unit tests for the `wiki_robot` module.
"""

import unittest
import datetime
import wiki_robot


class TestWikiRobot(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.name = "Alan Turing"
        self.date_of_birth = datetime.datetime.strptime("1912-06-23", "%Y-%m-%d").date()
        self.date_of_death = datetime.datetime.strptime("1954-06-07", "%Y-%m-%d").date()
        self.age = 41
        self.summary = "Alan Mathison Turing OBE FRS (/ˈtjʊərɪŋ/; 23 June 1912 – 7 June 1954) was an English mathematician, computer scientist, logician, cryptanalyst, philosopher, and theoretical biologist.[6] Turing was highly influential in the development of theoretical computer science, providing a formalisation of the concepts of algorithm and computation with the Turing machine, which can be considered a model of a general-purpose computer.[7][8][9] He is widely considered to be the father of theoretical computer science and artificial intelligence.[10]"
        self.scientist = wiki_robot.WikiScientist(self.name, self.date_of_birth, self.date_of_death, self.summary)

    def test_wiki_scientist(self):
        """Tests attributes of `wiki_robot.WikiScientist`"""
        scientist = wiki_robot.WikiScientist(self.name, self.date_of_birth, self.date_of_death, self.summary)
        self.assertEqual(scientist.name, self.name)
        self.assertEqual(scientist.date_of_birth, self.date_of_birth)
        self.assertEqual(scientist.date_of_death, self.date_of_death)
        self.assertEqual(scientist.age, self.age)
        self.assertEqual(scientist.summary, self.summary)
    
    def test_get_content(self):
        """Tests function `get_content` of robot."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        self.assertEqual(robot.get_content(self.name), self.scientist)
        robot.close_browser()
    
    def test_search_article(self):
        """Tests function `search_article` of robot."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        robot.open_browser()
        robot.search_article(self.name)
        self.assertEqual(robot.br.get_location(), "https://en.wikipedia.org/wiki/Alan_Turing")
        robot.close_browser()

    def test_get_location(self):
        """Tests function `get_location` of robot."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        robot.open_browser()
        robot.search_article(self.name)
        self.assertEqual(robot.get_location(), "https://en.wikipedia.org/wiki/Alan_Turing")
        robot.close_browser()
    
    def test_get_title(self):
        """Tests function `get_title` of robot."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        robot.open_browser()
        robot.search_article(self.name)
        self.assertEqual(robot.get_title(), "Alan Turing - Wikipedia")
        robot.close_browser()

    def test_get_domain(self):
        """Tests function `get_domain` of robot."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        self.assertEqual(robot.get_domain("https://en.wikipedia.org/wiki/Alan_Turing"), "wikipedia")

    def test_is_at_article(self):
        """Tests function `is_at_article` of robot."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        robot.open_browser()
        robot.search_article(self.name)
        self.assertEqual(robot.is_at_article(self.name), True)
        robot.search_article("Stephen Hawking")
        self.assertEqual(robot.is_at_article(self.name), False)
        robot.close_browser()
    
    def test_open_browser(self):
        """Tests function `open_browser` of robot."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        robot.open_browser()
        self.assertEqual(robot.br.get_browser_ids(), [1])
        robot.close_browser()

    def test_close_browser(self):
        """Tests function `close_browser` of robot."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        robot.open_browser()
        robot.open_browser()
        robot.close_browser()
        self.assertEqual(robot.br.get_browser_ids(), [])

    def test_is_browser_open(self):
        """Tests function `is_browser_open` of robot."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        robot.open_browser()
        self.assertEqual(robot.is_browser_open(), True)
        robot.close_browser()
        self.assertEqual(robot.is_browser_open(), False)

    def test_extract_from_article(self):
        """Tests function `extract_from_article` of robot."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        robot.open_browser()
        robot.search_article(self.name)
        self.assertEqual(robot.extract_from_article(self.name), self.scientist)
        robot.close_browser()

    def test_date_of_birth(self):
        """Tests if robot can retrieve the date of birth correctly."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        robot.open_browser()
        robot.search_article(self.name)
        self.assertEqual(robot._get_date_of_birth(), self.date_of_birth)
        robot.close_browser()
    
    def test_date_of_death(self):
        """Tests if robot can retrieve the date of death correctly."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        robot.open_browser()
        robot.search_article(self.name)
        self.assertEqual(robot._get_date_of_death(), self.date_of_death)
        robot.close_browser()
    
    def test_first_paragraph(self):
        """Tests if robot can retrieve the first paragraph correctly."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        robot.open_browser()
        robot.search_article(self.name)
        self.assertEqual(robot._get_first_paragraph(), self.summary)
        robot.close_browser()

    def test_biography_lookup(self):
        """Tests function `_biography_lookup` of robot."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        expected = 'xpath://table[@class="infobox biography vcard"]//th[contains(text(), "Awards")]//../td/span'
        self.assertEqual(robot._biography_lookup("Awards"), expected)
    
    def test_get_biography_date(self):
        """Tests function `_get_biography_date` of robot."""
        robot = wiki_robot.WikiScientistRobot("Test Robot")
        robot.open_browser()
        robot.search_article(self.name)
        self.assertEqual(robot._get_biography_date("Born"), self.date_of_birth)
        self.assertEqual(robot._get_biography_date("Died"), self.date_of_death)
        robot.close_browser()


if __name__ == "__main__":
    unittest.main()

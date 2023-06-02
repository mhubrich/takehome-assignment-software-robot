"""This script runs the Wiki-Scientist-Robot and creates a PDF report."""
from wiki_robot import WikiScientistRobot


SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"]


def main():
    robot = WikiScientistRobot("Wiki-Scientist-Robot")
    robot.run(SCIENTISTS, "report.pdf")


if __name__ == "__main__":
    main()

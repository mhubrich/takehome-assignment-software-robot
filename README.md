# Take-Home Assignment: Software Robot
This repository contains my solution to the technical take-home assignment below.

![Example](/examples/example.gif)

## The Task
The purpose of this software robot is to find key information about important scientists
and display it to the user.

When this robot is run, it should:

1. Introduce itself and explain the steps it's about to take.
2. Navigate to the wikipedia page of the scientists found in the list SCIENTISTS.
3. Retrieve the dates the scientists were born and died and calculate their age. Also, 
    retrieve the first paragraph of their wikipedia page.
4. Display all of this information to the user in an easily understood manner. 

### A few things to keep in mind
- This should be written as production level code. i.e. You would expect this code to
    pass a PR to get merged into main.
- As this is a software robot, it should not make use of any wikipedia API but it should 
    instead open a browser and navigate to wikipedia in the same manner a human would.
- The provided code can be added to, removed and changed as you see fit.
- Please use rpaframework to complete this task. Documentation for the provided 
    library can be found [here](https://rpaframework.org/#)

---

## Getting Started

### Installation
Install all dependencies with `pip install -r requirements.txt`.

Dependencies:
- `rpaframework`
- `rpaframework-assistant`

### Usage
Simply run `python main.py` to start the software robot.

### Tests
The module `test.py` contains a number of tests using Python's `unittest` framework.
To execute these tests, run `python -m unittest test.py`.

## Improvements
With additional time, I would include the following improvements:
- More test cases, for example unit tests for raised exceptions or integration tests.
- Prettify the first paragraph extracted from Wikipedia, for example removing citations.
- Prettify dialogs, for example using more styling elements.
- Prettify PDF report, for example creating a visually pleasing template that can be reused.

### Bonus
With additional time, I would work on the following features:
- Specify the language used on Wikipedia (note that other languages might use a different DOM structure).
- Provide a list of scientists to choose from, or an input field for a user to specift scientists.
- Include a picture of the scientist in the report.
- Support for scientists who are still alive, i.e. no date of death.
- Instead of saving the PDF report on the hard drive, send an email notification with the report (e.g. by using `RPA.Notifier`)

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

## Author
[Markus Hubrich](https://github.com/mhubrich)

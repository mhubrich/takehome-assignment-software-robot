"""Dialog Builder

This module exposes one function: show_dialog. The function is able to
build and display custom dialogs using the RPA.Assistant framework.
"""

from RPA.Assistant import Assistant


def show_dialog(body, title=None, header=None, file=None, button=None):
    """Displays a dialog with the given content.

    Note: at least `body` must be specified.

    Parameters
    ----------
    body : list
        A list of strings, which are added to the dialog
    title : str, optional
        A title of the dialog window
    header : str, optional
        A header at the top of the dialog
    file : str, optional
        A  path to a file
    button : str, optional
        A name of a button
    """

    assert isinstance(body, list)
    assert len(body) > 0
    assert all(isinstance(b, str) for b in body)
    assert (title is None or isinstance(title, str))
    assert (header is None or isinstance(header, str))
    assert (file is None or isinstance(file, str))
    assert (button is None or isinstance(button, str))

    dialog = Assistant()
    if header:
        dialog.add_heading(header)
    for text in body:
        dialog.add_text(text)
    if file:
        dialog.add_file(file)
    if button:
        dialog.add_submit_buttons(button)
    dialog.run_dialog(title=title)

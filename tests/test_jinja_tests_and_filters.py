from flaskext.genshi import render_template



def test_provides_jinja_tests_and_filters(app):
  with app.test_request_context():
    """Jinja tests and filters should be provided as context dictionaries."""

    rendered = render_template('jinja_tests_and_filters.html')
    expected_data = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                     '"http://www.w3.org/TR/html4/strict.dtd">\n'
                     '<p class="odd">\n'
                     '    Hello ...\n'
                     '  <span class="even">\n'
                     '      Hello ...\n'
                     '  </span>\n'
                     '</p>')

    assert rendered == expected_data

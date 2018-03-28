from flaskext.genshi import render_template



def test_provides_jinja_tests_and_filters(app):
    """Jinja tests and filters should be provided as context dictionaries."""
    with app.test_request_context():

        rendered = render_template('jinja_tests_and_filters.html')
        expected_data = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                         '"http://www.w3.org/TR/html4/strict.dtd">\n'
                         '<p class="odd">\n'
                         '    HELLO WORLD\n'
                         '  <span class="even">\n'
                         '      hello world\n'
                         '  </span>\n'
                         '</p>')

        assert rendered == expected_data

from flask_kajiki import render_template



def test_provides_jinja_tests_and_filters(app):
    """Jinja tests and filters should be provided as context dictionaries."""
    with app.test_request_context():

        rendered = render_template('jinja_tests_and_filters.html')
        # TODO DOCTYPE; see also render_args
        expected_data = ('<p class="odd">\n'
                         '    HELLO WORLD\n'
                         '  <span class="even">\n'
                         '      hello world\n'
                         '  </span>\n'
                         '    Hello...\n'
                         '    foo bar\n'
                         '    FooBar\n'
                         '</p>')

        assert rendered == expected_data

from genshi.filters import Translator
from flaskext.genshi import render_template



def test_does_translations(app):
    with app.test_request_context():
        """Callback interface is able to inject Translator filter"""

        genshi = app.extensions['genshi']
        @genshi.template_parsed
        def callback(template):
            Translator(lambda s: s.upper()).setup(template)

        rendered = render_template('i18n.html')
        expected = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                    '"http://www.w3.org/TR/html4/strict.dtd">\n'
                    '<p>HELLO!</p>')

        assert rendered == expected

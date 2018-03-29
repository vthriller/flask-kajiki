from kajiki import i18n
from flask_genshi import render_template


# TODO (document) request-aware i18ning?
i18n.gettext = lambda s: s.upper()


def test_does_translations(app):
    """Callback interface is able to inject Translator filter"""
    with app.test_request_context():

        rendered = render_template('i18n.html')
        expected = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                    '"http://www.w3.org/TR/html4/strict.dtd">\n'
                    '<p>HELLO!</p>')

        assert rendered == expected

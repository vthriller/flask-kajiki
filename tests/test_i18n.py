from kajiki import i18n
from flask import request
from flask_genshi import render_template


# N. B. settting i18n.gettext would affect tests from all modules,
# so we test for request path that only functions from this module could set
def gettext(s):
    if request.path == '/test_i18n':
        return s.upper()
    return s
i18n.gettext = gettext


def test_does_translations(app):
    """Callback interface is able to inject Translator filter"""
    with app.test_request_context(path='/test_i18n'):

        rendered = render_template('i18n.html')
        # TODO DOCTYPE; see also render_args
        expected = '<p>HELLO!</p>'

        assert rendered == expected

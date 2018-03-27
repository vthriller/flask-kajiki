from __future__ import with_statement

from genshi.filters import Transformer
from flask import current_app
from flaskext.genshi import render_template



def test_applies_method_filters(app):
  with app.test_request_context():
    """Method filters are applied for generated and rendered templates"""

    genshi = current_app.extensions['genshi']
    @genshi.filter('html')
    def prepend_title(template):
        return template | Transformer('head/title').prepend('Flask-Genshi - ')

    rendered = render_template('filter.html')
    expected = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                '"http://www.w3.org/TR/html4/strict.dtd">\n'
                '<html><head><title>Flask-Genshi - Hi!</title></head></html>')

    assert rendered == expected


def test_filters_per_render(app):
  with app.test_request_context():
    """Filters can be applied per rendering"""

    def prepend_title(template):
        return template | Transformer('head/title').append(' - Flask-Genshi')

    rendered = render_template('filter.html', filter=prepend_title)
    expected = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                '"http://www.w3.org/TR/html4/strict.dtd">\n'
                '<html><head><title>Hi! - Flask-Genshi</title></head></html>')

    assert rendered == expected

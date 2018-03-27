from __future__ import with_statement

from attest import Assert
from genshi.filters import Transformer
from flask import current_app
from flaskext.genshi import render_template

from tests.utils import flask_tests


filters = flask_tests()


@filters.test
def applies_method_filters():
    """Method filters are applied for generated and rendered templates"""

    genshi = current_app.extensions['genshi']
    @genshi.filter('html')
    def prepend_title(template):
        return template | Transformer('head/title').prepend('Flask-Genshi - ')

    rendered = Assert(render_template('filter.html'))
    expected = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                '"http://www.w3.org/TR/html4/strict.dtd">\n'
                '<html><head><title>Flask-Genshi - Hi!</title></head></html>')

    assert rendered == expected


@filters.test
def filters_per_render():
    """Filters can be applied per rendering"""

    def prepend_title(template):
        return template | Transformer('head/title').append(' - Flask-Genshi')

    rendered = Assert(render_template('filter.html', filter=prepend_title))
    expected = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                '"http://www.w3.org/TR/html4/strict.dtd">\n'
                '<html><head><title>Hi! - Flask-Genshi</title></head></html>')

    assert rendered == expected

from __future__ import with_statement

import pytest
from flaskext.genshi import render_response



def test_renders_strings(app, context):
  with app.test_request_context():
    """Strings can be rendered as templates directly"""

    rendered = render_response(string='The name is $name',
                                      context=context, method='text')

    assert rendered.data == 'The name is Rudolf'


def test_fails_without_template_or_string(app, context):
  with app.test_request_context():
    """A template or string must be provided to render"""

    with pytest.raises(RuntimeError):
        render_response(context=context, method='text')

# -*- coding: utf-8 -*-
"""
    flask_kajiki
    ~~~~~~~~~~~~

    An extension to Flask for easy Genshi templating.

    :copyright: (c) 2010 by Dag Odenhall <dag.odenhall@gmail.com>.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

from collections import defaultdict
import os.path
from warnings import warn
from inspect import getargspec

from kajiki import TextTemplate, XMLTemplate, FileLoader
from werkzeug import cached_property
from flask import current_app


# there's more to Jinja context than just environment,
# but apparently the only thing jinja filters currently care about is this (and also whether autoescaping is on),
# hence these shims.
# XXX this does not take custom jinja filters into account, although I don't expect Genshi-minded users of @jinja2.contextfilter any time soon.
class FakeJinjaContext:
    def __init__(self, env):
        self.environment = env
class FakeJinjaEvalContext:
    def __init__(self, env):
        self.environment = env
        # Flask set this one explicitly
        self.autoescape = env.autoescape


class Genshi(object):
    """Initialize extension.

    ::

        app = Flask(__name__)
        genshi = Genshi(app)

    .. versionchanged:: 0.4
        You can now initialize your application later with :meth:`init_app`.

    """

    def __init__(self, app=None):

        if app is not None:
            self.init_app(app)

        #: A callable for Genshi's callback interface, called when a template
        #: is loaded, with the template as the only argument.
        #:
        #: :meth:`template_parsed` is a decorator for setting this.
        #:
        #: .. versionadded:: 0.5
        self.callback = None

        #: What method is used for an extension.
        self.extensions = {
            'html': 'html',
            'xml': 'xml',
            'txt': 'text',
            'js': 'js',
            'css': 'css',
            'svg': 'svg'
        }

        #: Render methods.
        #:
        #: .. versionchanged:: 0.3 Support for Javascript and CSS.
        #: .. versionchanged:: 0.4 Support for SVG.
        self.methods = {
            'html': {
                'serializer': 'html',
                'doctype': 'html',
            },
            'html5': {
                'serializer': 'html',
                'doctype': 'html5',
            },
            'xhtml': {
                'serializer': 'xhtml',
                'doctype': 'xhtml',
                'mimetype': 'application/xhtml+xml'
            },
            'xml': {
                'serializer': 'xml',
                'mimetype': 'application/xml'
            },
            'text': {
                'serializer': 'text',
                'mimetype': 'text/plain',
                'class': TextTemplate
            },
            'js': {
                'serializer': 'text',
                'mimetype': 'application/javascript',
                'class': TextTemplate
            },
            'css': {
                'serializer': 'text',
                'mimetype': 'text/css',
                'class': TextTemplate
            },
            'svg': {
                'serializer': 'xml',
                'doctype': 'svg',
                'mimetype': 'image/svg+xml'
            }
        }

    def init_app(self, app):
        """Initialize a :class:`~flask.Flask` application
        for use with this extension. Useful for the factory pattern but
        not needed if you passed your application to the :class:`Genshi`
        constructor.

        ::

            genshi = Genshi()

            app = Flask(__name__)
            genshi.init_app(app)

        .. versionadded:: 0.4

        """
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['genshi'] = self
        self.app = app

    def template_parsed(self, callback):
        """Set up a calback to be called with a template when it is first
        loaded and parsed. This is the correct way to set up the
        :class:`~genshi.filters.Translator` filter.

        .. versionadded:: 0.5

        """
        self.callback = callback
        return callback

    @cached_property
    def template_loader(self):
        """A :class:`genshi.template.TemplateLoader` that loads templates
        from the same places as Flask.

        """
        path = os.path.join(
                self.app.root_path, self.app.template_folder)
        return FileLoader(path,
                              # TODO
                              #auto_reload=self.app.debug,
                              #callback=self.callback,
                         )

    def _method_for(self, template, method=None):
        """Selects a method from :attr:`Genshi.methods`
        based on the file extension of ``template``
        and :attr:`Genshi.extensions`, or based on ``method``.

        """
        if method is None:
            ext = os.path.splitext(template)[1][1:]
            return self.extensions[ext]
        return method


def generate_template(template=None, context=None,
                      method=None, string=None):
    """Creates a Genshi template stream that you can
    run filters and transformations on.

    """
    genshi = current_app.extensions['genshi']
    method = genshi._method_for(template, method)
    class_ = genshi.methods[method].get('class', XMLTemplate)

    filters = current_app.jinja_env.filters.copy()
    for name, f in filters.items():
        if getattr(f, 'environmentfilter', False):
            filters[name] = (lambda f: lambda *args, **kw: f(current_app.jinja_env, *args, **kw))(f)
        elif getattr(f, 'contextfilter', False):
            filters[name] = (lambda f: lambda *args, **kw: f(FakeJinjaContext(current_app.jinja_env), *args, **kw))(f)
        elif getattr(f, 'evalcontextfilter', False):
            filters[name] = (lambda f: lambda *args, **kw: f(FakeJinjaEvalContext(current_app.jinja_env), *args, **kw))(f)

    context = context or {}
    for key, value in current_app.jinja_env.globals.items():
        context.setdefault(key, value)
    context.setdefault('filters', filters)
    context.setdefault('tests', current_app.jinja_env.tests)
    for key, value in filters.items():
        context.setdefault(key, value)
    for key, value in current_app.jinja_env.tests.items():
        context.setdefault('is%s' % key, value)
    current_app.update_template_context(context)

    if template is not None:
        # TODO cls=class_
        template = genshi.template_loader.load(template)
    elif string is not None:
        template = class_(string)
    else:
        raise RuntimeError('Need a template or string')

    return template(context)


def render_template(template=None, context=None,
                    method=None, string=None):
    """Renders a template to a string."""
    genshi = current_app.extensions['genshi']
    method = genshi._method_for(template, method)
    template = generate_template(template, context, method, string)
    # TODO kajiki has no arguments for the serializer
    #render_args = dict(method=genshi.methods[method]['serializer'])
    #if 'doctype' in genshi.methods[method]:
    #    render_args['doctype'] = genshi.methods[method]['doctype']
    #return template.render(**render_args)
    return template.render()


def render_response(template=None, context=None,
                    method=None, string=None):
    """Renders a template and wraps it in a :attr:`~flask.Flask.response_class`
    with mimetype set according to the rendering method.

    """
    genshi = current_app.extensions['genshi']
    method = genshi._method_for(template, method)
    mimetype = genshi.methods[method].get('mimetype', 'text/html')
    template = render_template(template, context, method, string)
    return current_app.response_class(template, mimetype=mimetype)


def render(template, **context):
    """Render a template to a response object, passing the context as
    keyword arguments. Shorthand for
    ``render_response(template, dict(**context))``.

    .. versionadded:: 0.6

    """
    return render_response(template, context)

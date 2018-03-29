from flask_genshi import render_response



def test_updates_context(app):
    """Render calls update the template context with context processors"""
    with app.test_request_context():

        @app.context_processor
        def inject_rudolf():
            return dict(rudolf='The red-nosed reindeer')

        rendered = render_response('context.html')

        # TODO DOCTYPE; see also render_args
        expected_data = b'<pre>rudolf = The red-nosed reindeer</pre>'

        assert rendered.mimetype == 'text/html'
        assert rendered.data == expected_data

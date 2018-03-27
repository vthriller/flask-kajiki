from flaskext.genshi import render_response



def test_updates_context(app):
    with app.test_request_context():
        """Render calls update the template context with context processors"""

        @app.context_processor
        def inject_rudolf():
            return dict(rudolf='The red-nosed reindeer')

        render_response('context.html')

from flaskext.genshi import render_response



def test_updates_context(app):
    """Render calls update the template context with context processors"""
    with app.test_request_context():

        @app.context_processor
        def inject_rudolf():
            return dict(rudolf='The red-nosed reindeer')

        render_response('context.html')

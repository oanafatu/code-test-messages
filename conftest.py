import pytest


@pytest.yield_fixture(scope='session')
def app():

    from run import app

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture(scope='session')
def client(app):
    # db required as function argument to indicate fixture order for PyTest
    return app.test_client(use_cookies=False)

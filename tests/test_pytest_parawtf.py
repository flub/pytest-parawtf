import pytest


pytest_plugins = 'pytester'


SPELLINGS = ['params',
             'parametrize',
             'parameterize',
             'parametrise',
             'parameterise']


@pytest.fixture(params=SPELLINGS)
def spelling(request):
    return request.param


def test_mark(testdir, spelling):
    testdir.makepyfile("""
        import pytest
        @pytest.mark.%s('a', [0, 1])
        def test_foo(a):
            pass
    """ % spelling)
    result = testdir.inline_run()
    result.assertoutcome(passed=2)


def test_metafunc(testdir, spelling):
    testdir.makeconftest("""
        def pytest_generate_tests(metafunc):
            metafunc.%s('a', [0, 1])
    """ % spelling)
    testdir.makepyfile("""
        def test_foo(a):
            pass
    """)
    result = testdir.inline_run()
    result.assertoutcome(passed=2)

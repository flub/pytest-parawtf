import pytest                   # noqa


SPELLINGS = ['params',
             'parametrize',
             'parameterize',
             'parametrise',
             'parameterise']


def pytest_configure(config):
    python_plugin = config.pluginmanager.getplugin('python')
    hook_caller = config.pluginmanager.hook.pytest_generate_tests
    hook_caller._remove_plugin(python_plugin)
    for name in SPELLINGS:
        if not hasattr(python_plugin.Metafunc, name):
            setattr(python_plugin.Metafunc, name,
                    python_plugin.Metafunc.parametrize)


def pytest_generate_tests(metafunc):
    for marker in metafunc.definition.iter_markers():
        if marker.name not in SPELLINGS:
            continue
        metafunc.parametrize(*marker.args, **marker.kwargs)

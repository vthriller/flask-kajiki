from attest import Tests, AssertImportHook

AssertImportHook.disable()

all = Tests(['tests.test_rendering.rendering',
             'tests.test_filters.filters',
             'tests.test_context_processors.contexts',
             'tests.test_strings.strings',
             'tests.test_jinja_tests_and_filters.jinja',
             'tests.test_i18n.i18n',
             'tests.test_signals.signals',
            ])

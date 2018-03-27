from attest import Tests, AssertImportHook

AssertImportHook.disable()

all = Tests(['tests.rendering.rendering',
             'tests.filters.filters',
             'tests.context_processors.contexts',
             'tests.strings.strings',
             'tests.jinja_tests_and_filters.jinja',
             'tests.i18n.i18n',
             'tests.signals.signals',
            ])

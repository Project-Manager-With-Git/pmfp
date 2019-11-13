from voluptuous import Schema, All, ALLOW_EXTRA, Range

config_schema = Schema(
    {
        'DEBUG': bool,
        'HOST': str,
        'SECRET_KEY': str,
        'PORT': All(int, Range(min=1, max=10000))
    },
    extra=ALLOW_EXTRA
)

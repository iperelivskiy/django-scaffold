
PIPELINE_CSS = {
    'main': {
        'source_filenames': (
            'plugins/humane/themes/jackedup.css',
            'css/main.css',
        ),
        'output_filename': 'css/main.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'admin': {
        'source_filenames': (
            'css/admin.css',
        ),
        'output_filename': 'css/admin.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}

PIPELINE_JS = {
    'modernize': {
        'source_filenames': (
            'js/modernize/modernizr-2.6.2-respond-1.1.0.min.js',
            'js/modernize/es5-shim.js',
            'js/modernize/json2.js',
            'js/modernize/console.js',
        ),
        'output_filename': 'js/modernize.js',
    },
    'main': {
        'source_filenames': (
            'vendor/jquery/jquery-1.9.1.js',
            'vendor/underscore.js',
            'vendor/bootstrap/js/bootstrap-dropdown.js',
            'plugins/humane/humane.js',
            'js/main.js',
        ),
        'output_filename': 'js/main.js',
    }
}

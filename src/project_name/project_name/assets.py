
from django_assets import Bundle, register


register('main_js', Bundle(
    'js/libs/jquery-1.7.1.min.js',
    #'js/libs/jquery-ui-1.8.18.min.js',
    #'js/libs/underscore.min.js',
    'js/plugins.js',
    output='assets/js/main_bundle.js'
))

register('main_css', 'css/main.css', output='assets/css/main_bundle.css')

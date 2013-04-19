
/*global log, alert, _, humane, Messages*/

/*jshint expr:true */
!(function($, window, document, undefined) {
    "use strict";

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        },
        complete: function(jqXHR, textStatus) {
            var data;

            try {
                data = $.parseJSON(jqXHR.responseText);
            } catch (e) {}

            if (data) {
                if (data.location) {
                    window.location = data.location;
                }

                if ($.isArray(data.messages)) {
                    _.each(data.messages, function(message) {
                        var type = message[1];

                        if (typeof type === 'string') {
                            var tags = type.split(' ');
                            type = '';
                            _.each(tags, function(tag) {
                                if (Messages.tags.indexOf(tag) !== -1) {
                                    type += ' ' + Messages.classprefix + tag;
                                } else {
                                    type += ' ' + tag;
                                }
                            });
                        }

                        Messages.add(null, message[0], {addnCls: type});
                    });
                }
            }
        }
    });

    /*jshint supernew:true*/
    window.Messages = new (function() {
        this.add = function(tag, message, options) {
            var messenger = humane.create($.extend({
                addnCls: 'humane-jackedup-' + tag,
                baseCls: 'humane-jackedup',
                clickToClose: true,
                timeout: 3000,
                waitForMove: true
            }, options));

            messenger.log(message);
        };

        this.tags = ['info', 'success', 'debug', 'warning', 'error'];
        this.classprefix = 'humane-jackedup-';

        this.info = function(message, options) {
            return this.add('info', message, options);
        };

        this.success = function(message, options) {
            return this.add('success', message, options);
        };

        this.debug = function(message, options) {
            return this.add('debug', message, options);
        };

        this.warning = function(message, options) {
            return this.add('warning', message, options);
        };

        this.error = function(message, options) {
            return this.add('error', message, options);
        };
    })();

})(window.jQuery, window, document);

"Typeahead extras";

/*global _*/
/*jshint expr:true*/
!(function($, window, document) {
    "use strict";

    if ($.extras === undefined) {
        $.extras = {};
    }

    function typeahead($el, options) {
        "Typeahead with extra options";

        // Extra options:
        // * titleGetter - callback or string, returning title of an object.
        // * onSelect - callback, called when item is chosen from typeahead.
        // * onReset - callback, fired when input is about to be reset.
        // * fitWidth - bool, whether to resize dropdown to width of input.
        // * strict - bool, detects whether to perform a reset
        //   of input if it contains value that haven't been selected via
        //   typeahead.
        // * stripHTML - bool, whether to strip html on updating input.
        // * highlighter -bool, whether to use highlighter.

        options = options || {};

        var extraOptions = $.extend({
            titleGetter: function(obj) {return obj.name || obj.title || 'Undefined title';},
            onSelect: function(obj) {},
            onReset: function() {},
            fitWidth: true,
            strict: false,
            stripHTML: true,
            highlighter: false
        }, options.extra);

        var source = options.source;

        delete options.extra;
        delete options.source;
        delete options.updater;

        if (typeof extraOptions.titleGetter === 'string') {
            var titleAttribute = extraOptions.titleGetter;
            extraOptions.titleGetter = function(obj) {
                return obj[titleAttribute] || 'Undefined title';
            };
        }

        function extraSource(q, process) {
            var extraProcess = function(objects, contextData) {
                process(_.map(objects || [], function (obj) {
                    obj.__title__ = extraOptions.titleGetter(obj, contextData);

                    var
                        title = obj.__title__,
                        lowerTitle = title.toLowerCase(),
                        objstr = JSON.stringify(obj);

                    return {
                        toString: function() {
                            return objstr;
                        },
                        toLowerCase: function() {
                            return lowerTitle;
                        },
                        indexOf: function() {
                            return String.prototype.indexOf.apply(title,
                                                                  arguments);
                        },
                        replace: function() {
                            return String.prototype.replace.apply(title,
                                                                  arguments);
                        }
                    };
                }));
            };

            var contextData = {q: q};

            if ($.isFunction(source)) {
                var objects = source(q, extraProcess);
                if ($.isArray(objects)) {
                    contextData.source = objects;
                    extraProcess(objects, contextData);
                }
            } else {
                contextData.source = source;
                extraProcess(source, contextData);
            }
        }

        function updater(item) {
            var
                value = 'Undefined title',
                obj;

            try {
                obj = JSON.parse(item);
            } catch (e) {}

            if (obj.__title__) {  // Object unpickled successfully.
                extraOptions.onSelect(obj);
                value = obj.__title__;
            }

            if (extraOptions.stripHTML) {
                value = $('<div/>').html(value).text();
            }

            $el.data('selectedValue', value);
            return value;
        }

        if (!extraOptions.highlighter) {
            options.highlighter = function(item) {
                // Dummy highlighter.
                return item.replace();
            };
        }

        var api = $el.typeahead($.extend({
            source: extraSource,
            updater: updater
        }, options))
        .on('change copy paste cut blur', function() {
            if (extraOptions.strict) {
                // Check equality of current value of input and last selected
                // value via typeahead. If they are not equal then perform
                // reset of input as it may mean invalid user input.
                var
                    self = $(this),
                    curValue = self.val(),
                    selectedValue = self.data('selectedValue');

                if (curValue !== selectedValue) {
                    // Input is in inconsistent state.
                    // Reset input and fire a callback.
                    extraOptions.onReset.call(api);
                    self.val('');
                    self.removeData('selectedValue');
                }
            }
        }).data('typeahead');

        if (extraOptions.fitWidth) {
            // Patch show function.
            var
                superShow = $.proxy(api.show, api),
                show = function () {
                    superShow();
                    this.$menu.css('minWidth', this.$element.outerWidth());
                    // Tip: make use of box-sizing:border-box css property on
                    // your typeahead dropdown to exact fit the width of input.
                    // Works in all modern browsers.
                    return this;
                };

            api.show = $.proxy(show, api);
        }

        return $el;
    }

    typeahead.ajax = function($el, url, options) {
        "Typeahed ajax extension";

        options = options || {};

        var
            extraOptions = options.extra || {},
            cache = {},
            ajaxOptions = $.extend({
                data: null,
                sourceGetter: 'results',  // Callable or string.
                cacheKey: false
            }, extraOptions.ajax);

        delete extraOptions.ajax;

        if (typeof ajaxOptions.sourceGetter === 'string') {
            var responseAttribute = ajaxOptions.sourceGetter;
            ajaxOptions.sourceGetter = function(response) {
                return response[responseAttribute] || [];
            };
        }

        return typeahead($el, $.extend({
            source: function (q, process) {
                var
                    data = $.isFunction(ajaxOptions.data) ?
                        ajaxOptions.data(q) : ajaxOptions.data,
                    contextData = {
                        q: q,
                        data: data
                    };

                var cacheKey = ajaxOptions.cacheKey;
                if ($.isFunction(cacheKey)) {
                    cacheKey = cacheKey(contextData);
                }

                if (cacheKey && (cacheKey in cache)) {
                    var objects = cache[cacheKey];
                    contextData.source = objects;
                    contextData.fromCache = true;
                    process(objects, contextData);
                    return;
                }

                if (data !== false) {
                    $.get(url, data).done(function(response) {
                        var objects = ajaxOptions.sourceGetter(response);
                        if ($.isArray(objects)) {
                            contextData.source = objects;
                            process(objects, contextData);
                            if (cacheKey) {
                                cache[cacheKey] = objects;
                            }
                        }
                    });
                }
            },
            matcher: function() {
                // Assuming remote source is already filtered,
                // so all results match.
                return true;
            },
            minLength: 2
        }, options));
    };

    $.extras.typeahead = typeahead;

    // Typeahead ajax widget for foreign keys.

    var ajaxTypeaheadInit = function($el, event) {
        var
            $id = $el.find('input[type="hidden"]'),
            $input = $el.find('input[type="text"]');

        if ($input.data('typeahead')) {
            return;
        }

        if (event) {
            event.preventDefault();
        }

        var
            id = $id.val().trim(),
            input = $input.val().trim();

        // If one of id or input or both are somehow empty then
        // clear them both for consistency.
        if (!id || !input) {
            $id.val('');
            $input.val('');
            // Set for correct internal typeahead state.
            $input.data('selectedValue', '');
        } else {
            // Set for correct internal typeahead state.
            $input.data('selectedValue', input);
        }

        typeahead.ajax($input, $el.data('url'), {
            extra: {
                onSelect: function(obj) {
                    $id.val(obj.id);
                },
                onReset: function() {
                    $id.val('');
                },
                strict: true,
                ajax: {
                    data: function(q) {
                        if (q.trim()) {
                            return {q: q.trim()};
                        }

                        return false;  // Mean ajax call won't be performed.
                    },
                    cacheKey: function(contextData) {
                        if (contextData.data) {
                            // About to send request for remote source.
                            // Use request params as cache key.
                            return contextData.data.q;
                        }
                    }
                }
            }
        });
    };

    $(document).on('focus', '[data-widget="ajax-typeahead"]', function (e) {
        ajaxTypeaheadInit($(this), e);
    });

    $(function() {
        $('[data-widget="ajax-typeahead"]').each(function() {
            ajaxTypeaheadInit($(this));
        });
    });

})(window.jQuery, window, document, undefined);

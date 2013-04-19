"Qtip based dropdown";

/*global _, log*/
/*jshint expr:true*/
!(function($, window, document, undefined) {
    "use strict";

    var
        toggle = '[data-toggle="qtip-dropdown"]',
        eventTypes = ['tooltipshow', 'tooltipfocus', 'tooltipmove',
                      'tooltipvisible', 'tooltiphide', 'tooltipblur',
                      'tooltiphidden', 'tooltiprender'];


    function clearDropdowns(event) {
        $(toggle).each(function() {
            var
                $toggle = $(this),
                api = $toggle.data('qtip');

            $toggle.removeClass('active');
            api && api.hide();
        });
    }

    function toggleDropdown(event) {
        // Close Bootstrap dropdowns.
        $('[data-toggle=dropdown]').each(function () {
            getBootstrapParent($(this)).removeClass('open');
        });

        var $this = $(this),
            $target = getTarget($this),
            api = $this.data('qtip') || $target.data('qtip'),
            active = $this.blur().hasClass('active');

        // Deactivate others toggles.
        $('.active' + toggle).not($this).removeClass('active');

        if (active) {
            event.stopImmediatePropagation();
            event.preventDefault();
            api && api.hide();
            $this.removeClass('active');
        } else {
            if (passTest($this, $target)) {
                var options = getOptions($this, $target);

                if (!api) {
                    api = $('<div/>').qtip($.extend(true, {
                        content: ' ',
                        position: {
                            viewport: $('#wrap'),
                            adjust: {
                                method: 'shift flip'
                            }
                        },
                        show: {
                            delay: 0,
                            event: false,
                            solo: true,
                            effect: false
                        },
                        hide: {
                            event: false,
                            effect: false
                        },
                        style: {
                            classes: 'qtip-dropdown',
                            def: false,
                            tip: {
                                corner: false
                            }
                        }
                    }, options)).qtip('api');

                    api.render(0);
                }

                event.stopImmediatePropagation();
                event.preventDefault();
                bindAPI($this, api);
                bindAPI($target, api);

                api.set({
                    'position.target': $this,
                    'position.my': options.position.my,
                    'position.at': options.position.at,
                    'position.adjust.x': options.position.adjust.x,
                    'position.adjust.y': options.position.adjust.y
                });

                api.show();
                $this.addClass('active');
            } else {
                unbindAPI($this);
                unbindAPI($target);
            }
        }
    }


    function keydown(event) {
        if (event.keyCode === 27) {
            clearDropdowns();
        }
    }


    function getTarget($this) {
        var selector = $this.attr('data-target');

        if (! selector) {
            selector = $this.attr('href');
            selector = selector && /#/.test(selector) && selector.replace(/.*(?=#[^\s]*$)/, '');  //strip for ie7
        }

        return $(selector);
    }


    function passTest($toggle, $target) {
        function getTest($this) {
            var test = $this.data('if');

            if (typeof test === 'string') {
                var
                    attrs = test.split('.'),
                    ref = window;

                try {
                    _.each(attrs, function(attr) {
                        ref = ref[attr];
                    });

                    test = ref;
                } catch (e) {}
            }

            if ($.isFunction(test)) {
                return test;
            }

            return function() {
                return true;
            };
        }

        var
            t1 = getTest($toggle),
            t2 = getTest($target);

        return !!(t1($toggle, $target) && t2($toggle, $target));
    }


    function getOptions($toggle, $target) {
        var options = $.extend(true, {}, $target.data(), $toggle.data());

        _.each(['action', 'if', 'target', 'toggle', 'qtip'], function(option) {
            delete options[option];
        });

        options.position = {
            my: 'top left',
            at: 'bottom left',
            adjust: {
                x: 0,
                y: 0
            }
        };

        if (options.positionAt) {
            options.position.at = options.positionAt;
            delete options.positionAt;
        }

        if (options.positionMy) {
            options.position.my = options.positionMy;
            delete options.positionMy;
        }

        if ($target.length) {
            options.content = $target;
        }

        return options;
    }


    function getBootstrapParent($this) {
        var
            selector = $this.attr('data-target'),
            $parent;

        if (!selector) {
            selector = $this.attr('href');
            selector = selector && /#/.test(selector) && selector.replace(/.*(?=#[^\s]*$)/, '');  //strip for ie7
        }

        $parent = $(selector);
        $parent.length || ($parent = $this.parent());

        return $parent;
    }


    function bindAPI($el, api) {
        $el.data('qtip', api);

        _.each(eventTypes, function(eventType) {
            api.elements.tooltip.one(eventType, function(event) {
                $el.trigger(eventType.replace('tooltip', 'dropdown'));
            });
        });
    }


    function unbindAPI($el) {
        // TODO: More graceful unbind.
        $el.removeData('qtip');
    }

    $(document)
        .on('click.qtip-dropdown touchstart.qtip-dropdown', clearDropdowns)
        .on('click.dropdown.data-api touchstart.dropdown.data-api',
            '[data-toggle=dropdown]', clearDropdowns)

        .on('touchstart.qtip-dropdown', '.dropdown-menu',
            function(event) { event.stopPropagation(); })

        // Prevent closing qtip-dropdown when clicking on dropdown itself;
        .on('click.qtip-dropdown touchstart.qtip-dropdown',
            '.qtip-dropdown', function(event) { event.stopPropagation(); })

        .on('click.qtip-dropdown touchstart.qtip-dropdown', toggle,
            toggleDropdown)

        .on('keydown.qtip-dropdown touchstart.qtip-dropdown', keydown);

})(window.jQuery, window, document);

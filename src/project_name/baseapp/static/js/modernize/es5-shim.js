
/*jshint expr:true*/
!(function() {
    'use strict';

    var
        call = Function.prototype.call,
        prototypeOfObject = Object.prototype,
        _toString = call.bind(prototypeOfObject.toString);


    // Check failure of by-index access of string characters (IE < 9)
    // and failure of `0 in boxedString` (Rhino)
    var boxedString = Object("a"),
        splitString = boxedString[0] !== "a" || !(0 in boxedString);

    // ES5 15.5.4.20
    // http://es5.github.com/#x15.5.4.20
    var ws = "\x09\x0A\x0B\x0C\x0D\x20\xA0\u1680\u180E\u2000\u2001\u2002\u2003" +
        "\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u202F\u205F\u3000\u2028" +
        "\u2029\uFEFF";
    if (!String.prototype.trim || ws.trim()) {
        // http://blog.stevenlevithan.com/archives/faster-trim-javascript
        // http://perfectionkills.com/whitespace-deviations/
        ws = "[" + ws + "]";
        var trimBeginRegexp = new RegExp("^" + ws + ws + "*"),
            trimEndRegexp = new RegExp(ws + ws + "*$");
        String.prototype.trim = function trim() {
            if (this === undefined || this === null) {
                throw new TypeError("can't convert "+this+" to object");
            }
            return String(this)
                .replace(trimBeginRegexp, "")
                .replace(trimEndRegexp, "");
        };
    }

    // ES5 15.4.4.14
    // http://es5.github.com/#x15.4.4.14
    // https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Array/indexOf
    if (!Array.prototype.indexOf || ([0, 1].indexOf(1, 2) !== -1)) {
        Array.prototype.indexOf = function indexOf(sought /*, fromIndex */ ) {
            var self = splitString && _toString(this) === "[object String]" ?
                    this.split("") :
                    toObject(this),
                length = self.length >>> 0;

            if (!length) {
                return -1;
            }

            var i = 0;
            if (arguments.length > 1) {
                i = toInteger(arguments[1]);
            }

            // handle negative indices
            /*jshint plusplus:false*/
            i = i >= 0 ? i : Math.max(0, length + i);
            for (; i < length; i++) {
                if (i in self && self[i] === sought) {
                    return i;
                }
            }
            return -1;
        };
    }

    // ES5 15.4.4.15
    // http://es5.github.com/#x15.4.4.15
    // https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Array/lastIndexOf
    if (!Array.prototype.lastIndexOf || ([0, 1].lastIndexOf(0, -3) !== -1)) {
        Array.prototype.lastIndexOf = function lastIndexOf(sought /*, fromIndex */) {
            var self = splitString && _toString(this) === "[object String]" ?
                    this.split("") :
                    toObject(this),
                length = self.length >>> 0;

            if (!length) {
                return -1;
            }
            var i = length - 1;
            if (arguments.length > 1) {
                i = Math.min(i, toInteger(arguments[1]));
            }
            // handle negative indices
            i = i >= 0 ? i : length - Math.abs(i);
            /*jshint plusplus:false*/
            for (; i >= 0; i--) {
                if (i in self && sought === self[i]) {
                    return i;
                }
            }
            return -1;
        };
    }

    // ES5 9.9
    // http://es5.github.com/#x9.9
    var toObject = function (o) {
        if (o === null || o === undefined) {
            // this matches both null and undefined
            throw new TypeError("can't convert " + o + " to object");
        }
        return Object(o);
    };

    // ES5 9.4
    // http://es5.github.com/#x9.4
    // http://jsperf.com/to-integer

    function toInteger(n) {
        n = +n;
        if (n !== n) { // isNaN
            n = 0;
        } else if (n !== 0 && n !== (1/0) && n !== -(1/0)) {
            n = (n > 0 || -1) * Math.floor(Math.abs(n));
        }
        return n;
    }
})();

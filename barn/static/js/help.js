var $ = require('jquery');

var Help = {
    init: function(options, elem) {
        var t = this;
        this.options = $.extend({}, this.options, options);

        this.elem = elem;
        this.$elem = $(elem);

        this.positioned = false;

        $(elem).text(t.options.label);

        $(elem).after('<div></div>').next()
            .attr('class', 'help_box')
            .attr('style', '')
            .text(t.options.text);

        $(elem).hover(
            function() {
                if (!t.positioned) {
                    $(this).next().position({
                        'my': 'left bottom', 
                        'at': 'right top', 
                        'of': $(this),
                    });

                    t.positioned = true;
                }
                $(this).next().show();
            },
            function() {
                $(this).next().hide();
            }
        );
    },

    options: {
        text: '',
        label: '?',
    },

};

$.plugin('help', Help);

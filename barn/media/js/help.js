var Help = {
    init: function(options, elem) {
        var t = this;
        this.options = $.extend({}, this.options, options);

        this.elem = elem;
        this.$elem = $(elem);

        this.positioned = false;

        $(elem).after('<div></div>').next()
            .attr('class', 'help_box')
            .attr('style', '')
            .text(t.options.text);

        /*
        $(elem).click(function() {
            if (!t.positioned) {
                $(this).next().position({
                    'my': 'left bottom', 
                    'at': 'right top', 
                    'of': $(this),
                });

                t.positioned = true;
            }
            $(this).next().toggle();
        });
          */
        $(elem).hover(
            function() {
                if (!t.positioned) {
                    $(this).next().position({
                        'my': 'left bottom', 
                        'at': 'right top', 
                        'of': $(this),
                        /*'offset': '10 0',*/
                    });

                    t.positioned = true;
                }
                $(this).next().toggle();
            },
            function() {
                $(this).next().toggle();
            }
        );
    },

    options: {
        text: 'heeeeelp',
    },

};

$.plugin('help', Help);

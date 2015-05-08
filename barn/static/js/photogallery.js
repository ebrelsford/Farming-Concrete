//
// photogallery
//

var $ = require('jquery');

require('colorbox');

$(document).ready(function () {
    $('.photo-gallery a').colorbox({
        rel: 'gal',
    });
});

//
// addsales
//

var $ = require('jquery');

function calculateTotal() {
    var total = $(':input[name=unit_price]').val() * $(':input[name=units_sold]').val();
    return Math.round(total * 100) / 100;
}

$(document).ready(function () {
    if ($('.add-sales').length > 0) {
        $(':input[name=unit_price],:input[name=units_sold]').keyup(function () {
            $(':input[name=total_price]').val(calculateTotal);
        });
    }
});

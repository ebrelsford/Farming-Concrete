//
// addsales
//

define(['jquery'], function ($) {

    function calculateTotal() {
        var total = $(':input[name=unit_price]').val() * $(':input[name=units_sold]').val();
        return Math.round(total * 100) / 100;
    }

    $(document).ready(function () {
        $(':input[name=unit_price],:input[name=units_sold]').keyup(function () {
            $(':input[name=total_price]').val(calculateTotal);
        });
    });

});

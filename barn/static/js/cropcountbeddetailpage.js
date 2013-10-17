//
// cropcountbeddetailpage
//
// Scripts for the cropcount bed detail page.
//

define(
    [
        // Requirements with exports
        'jquery',
        'django',
        'farmingconcrete',

        'select2'

    ], function ($, Django, FC) {

        $(document).ready(function () {
            $('#add-new-plant-type a').click(function () {
                $('#add-new-plant-type .adder').toggle();
                return false;
            });

            var add_plant_type_url = Django.url('farmingconcrete_varieties_add');

            /*
             * Add plant type when form is submitted.
             */
            $('form').submit(function (e) {
                var name = $('input[name="new-plant-type"]').val();
                FC.get_or_create_plant_type(add_plant_type_url, name, true, function () {});
            });

            /*
             * Make variety input select2-y
             */
            $('#id_variety').select2();

            /*
             * Add plant type when person tabs out of plant type field.
             */
            $(':input#id_variety_text').blur(function () {
                // only try to add plant type if autocomplete didn't get something
                if ($(':input#id_variety').val() !== '') {
                    return;
                }
                FC.get_or_create_plant_type(add_plant_type_url, $(this).val(), false, function () {});
            });
        });
    }
);

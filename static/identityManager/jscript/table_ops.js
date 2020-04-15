// A $( document ).ready() block.
// $(document).ready(function () {
//     console.log("ready!");
//
//     $("#wbdap_imuser_list_table tbody").loadData({
//         url: '/identityManager/api/users/?format=json',
//     });
//
//
//     $('#wbdap_table_pagination_previous').click(function () {
//         if (typeof($('#wbdap_table_pagination_previous').attr("url")) !== "undefined") {
//             $("#wbdap_imuser_list_table tbody").loadData({
//                 url: $('#wbdap_table_pagination_previous').attr("url"),
//             });
//         }
//     });
//
//     $('#wbdap_table_pagination_next').click(function () {
//         if (typeof ($('#wbdap_table_pagination_next').attr("url")) !== null) {
//             $("#wbdap_imuser_list_table tbody").loadData({
//                 url: $('#wbdap_table_pagination_next').attr("url"),
//             });
//         }
//     });
//
//
// });
//
//
// $(function () {
//     $('#wbdap_imuser_list_table tbody').on("click", 'a.editValues', function () {
//         alert('editing');
//
//         var target_row = $(this).parents('tr');
//         target_row.css({'background-color': '#c7efff'});
//         $(this).parents('tr').find('td').each(function () {
//             if ($(this).attr('class') !== "row_operations" && $(this).attr('class') !== "id") {
//                 var html = $(this).html();
//                 var input = $('<input class="editableColumnsStyle" type="text" />');
//                 input.val(html);
//                 $(this).html(input);
//             }
//         });
//
//         //change the icon and class of edit so that it can not be used to reedit
//     });
// })
//
// $.fn.loadData = function (options) {
//     // This is the easiest way to have default options.
//
//     var tablebody = this;
//     var custom_settings = $.extend({
//         // These are the defaults.
//         url: null,
//     }, options);
//
//     $.ajax({
//         url: custom_settings.url,
//         context: document.body,
//         success: function (data) {
//
//             results = data.results;
//             var next_link = data.next;
//             var previous_link = data.previous;
//             tablebody.empty();
//             $.each(results, function (k, jrow) {
//                 var newRowContent = "<tr>";
//                 $.each(jrow, function (jfield, jval) {
//                     newRowContent = newRowContent + '<td>' + jval + "</td>";
//                 });
//                 newRowContent = newRowContent + "<td class='row_operations'>";
//
//                 newRowContent = newRowContent + "<a class='editValues' \n" +
//                     "style=\"cursor: pointer\">\n" +
//                     "<i class=\"fa fa-pencil-alt\" aria-hidden=\"true\"#}\n" +
//                     "data-toggle=\"tooltip\"\n" +
//                     "data-placement=\"left\" title=\"Edit Row\"></i></a>";
//
//                 newRowContent = newRowContent + "<a class='deleteRow' " +
//                     "style=\"cursor: pointer\">\n" +
//                     "<i class=\"fa fa-trash-alt\"\n" +
//                     "style=\"color: red\"\n" +
//                     "data-href=\"delete\"\n" +
//                     "data-toggle=\"modal\"\n" +
//                     "data-target=\"#confirm-delete\"\n" +
//                     "title=\"Delete User\"></i></a>"
//
//
//                 newRowContent = newRowContent + "</td>";
//
//                 newRowContent = newRowContent + "</tr>";
//                 tablebody.append(newRowContent);
//             });
//             $('#wbdap_table_pagination_previous').attr('url', previous_link);
//             $('#wbdap_table_pagination_next').attr('url', next_link);
//         }
//     });
//
//
// };
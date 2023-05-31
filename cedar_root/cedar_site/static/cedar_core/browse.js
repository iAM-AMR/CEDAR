

/*

This function enables Data Tables in browse views.

The template must contain an element "orderByColumnNumber" that specifies the
initial column to order-by on document load. Column positions are zero indexed.

Example: <div id="orderByColumnNumber" style="display: none;">1</div>

*/


$(document).ready(function () {

    var orderbycol = document.getElementById("orderByColumnNumber").innerHTML;

    $('.browse-table').DataTable({
      "scrollY": "",
      "scrollCollapse": true,
      order: [[orderbycol, 'asc']],
    });

    $('.dataTables_length').addClass('bs-select');

  });
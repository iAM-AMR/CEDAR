$(document).ready(function () {
    $('.browse-table').DataTable({
      "scrollY": "100%",
      "scrollCollapse": true,
      order: [[1, 'asc']],
    });
    $('.dataTables_length').addClass('bs-select');
  });
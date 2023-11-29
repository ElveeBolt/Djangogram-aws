$('[data-modal-toggle]').on('click', function (event) {
    var action = $(this).attr("data-modal-attr-action");
    var title = $(this).attr("data-modal-attr-title");
    $('#popup-modal form').attr('action', action);
    $('#popup-modal #title').text(title);
});
$(document).ready(function() {
    $('#like-form').submit(function(event) {
      event.preventDefault();

      var form = $(this);
      var url = form.attr('action');
      var method = form.attr('method');
      var data = form.serialize();

      $.ajax({
        url: url,
        type: method,
        data: data,
        success: function(response) {
            $('#post-like-count span').html(response.count);
            if (response.status) {
                form.find('button').html('<i class="las la-thumbs-down"></i>Dislike')
            } else {
                form.find('button').html('<i class="las la-thumbs-up"></i>Like')
            }

        },
        error: function(xhr, status, error) {
          console.log(error);
        }
      });
    });
  });
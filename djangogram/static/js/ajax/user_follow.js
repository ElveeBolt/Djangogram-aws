$(document).ready(function() {
    $('#follow-form').submit(function(event) {
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
            if (response.status) {
                form.find('button').html('<i class="las la-thumbs-down"></i>Unfollow')
            } else {
                form.find('button').html('<i class="las la-thumbs-up"></i>Follow')
            }
        },
        error: function(xhr, status, error) {
          console.log(error);
        }
      });
    });
  });
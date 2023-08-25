$(document).ready(function(){
    $(document).on('submit', '#login-form', function(e){
        e.preventDefault();

        const token = $("#login-form [name='csrfmiddlewaretoken']").val()
        $.ajax({
            method:"POST",
            url: LOGIN_URL,
            data:{
                'email': $('#email').val(),
                'password': $('#password').val()
            },
            headers:{
                'X-CSRFToken': token
            },
            dataType:'json',
            success:function(response){
                if(response.success){
                    $('#response').html('logged in')
                }
            },
            error:function(response){
                const error = JSON.parse(response.responseText)
                alert(error.message)
            }
        })
    })
})
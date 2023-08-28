$(document).ready(
    $(document).on('submit','#registration-form',function(e){
        e.preventDefault()

        const token = $("#registration-form [name='csrfmiddlewaretoken']").val()
        $.ajax({
            method:"POST",
            url: REGISTRATION_URL,
            data:{
                'username' : $('#username').val(),
                'email' : $('#email').val(),
                'first_name' : $('#first_name').val(),
                'last_name' : $('#last_name').val(),
                'password' : $('#password').val(),
                'confirm_password' : $('#confirm_password').val()
            },
            headers:{
                'X-CSRFToken': token
            },
            dataType:'json',
            success:function(response){
                if(response.success){
                    $('#response').html('registration success')
                }
            },
            error:function(response){
                const error = JSON.parse(response.responseText)
                alert(error.message)
            }
        })
    })
)
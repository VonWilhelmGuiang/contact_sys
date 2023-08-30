$(document).ready(function(){

    const isJsonParsable = string => {
        let parsed = {}
        try {
            parsed = JSON.parse(string);
        } catch (e) {
            return false;
        }
        return parsed;
    }

    $(document).on('submit','#registration-form',function(e){
        e.preventDefault()

        toastr.options = {
            "positionClass" : "toast-top-right",
            "closeButton" : false,
            "debug" : false,
            "newestOnTop" : false,
            "progressBar" : false,
            "preventDuplicates" : false,
            "onclick" : null,
            "timeOut" : "2000",
        }

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
            beforeSend : function(){
                $('#registration-form #submit').prop("disabled",true)
            },
            success:function(response){
                if(response.success){
                    toastr.options.onHidden = ( 
                        ()=>{window.location.href = (LOGIN_URL) }
                    )
                    toastr.success('Registered Successful. Redirecting you to Login Page. Please wait')
                    
                    // clean form
                    $('#username').prop('disabled',true)
                    $('#email').prop('disabled',true)
                    $('#first_name').prop('disabled',true)
                    $('#last_name').prop('disabled',true)
                    $('#password').prop('disabled',true)
                    $('#confirm_password').prop('disabled',true)
                }else{
                    toastr.error("An error has occured. Please try again")
                }
            },
            error:function(response){
                try{
                    const error = JSON.parse(response.responseText)
                    const error_messages = isJsonParsable(error.message)

                    // populate each error
                    if(error_messages){
                        $.each(error_messages, function(fields,messages){
                            $.each(messages, function(index,err){
                                toastr.error(err.message)
                            })
                        })
                    }
                    else{
                        toastr.error(error.message)
                    }
                }catch(err){
                    toastr.error("An error has occured. Please try again")
                }finally{
                    $('#registration-form #submit').prop("disabled",false)
                }
            }
        })
    })
})
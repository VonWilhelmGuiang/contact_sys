$(document).ready(function(){
    $(document).on('submit', '#login-form', function(e){
        e.preventDefault();

        const token = $("#login-form [name='csrfmiddlewaretoken']").val()
        toastr.options = {
            "positionClass" : "toast-top-center",
            "closeButton" : false,
            "debug" : false,
            "newestOnTop" : false,
            "progressBar" : false,
            "preventDuplicates" : false,
            "onclick" : null,
            "timeOut" : "2000",
        }
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
            beforeSend : function(){
                $('#login-form #submit').prop("disabled",true)
            },
            success:function(response){
                if(response.success){
                    toastr.options.onHidden = ( 
                        ()=>{window.location.replace(CONTACT_PAGE) }
                    )
                    toastr.success('Logging in. Please wait')
                }else{
                    toastr.error("An error has occured. Please try again")
                }
            },
            error:function(response){
                try{
                    const error = JSON.parse(response.responseText)
                    toastr.error(error.message)
                }catch(err){
                    toastr.error("An error has occured. Please try again")
                }finally{
                    $('#login-form #submit').prop("disabled",false)
                }
            }
        })
    })
})
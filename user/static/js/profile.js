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

    // populate data to inputs
    $('#edit-user-form #username').val(USERNAME)
    $('#edit-user-form #email').val(EMAIL)
    $('#edit-user-form #first_name').val(FIRST_NAME)
    $('#edit-user-form #last_name').val(LAST_NAME)

    $(document).on('click','#view-profile-controller',function(){
        if(!$('#view-profile-container').is(':visible')){
            $("#edit-profile-container").slideToggle(function(){ 
                $("#view-profile-container").slideToggle()
            });
        }
    })
    
    $(document).on('click','#edit-profile-controller',function(){
        if(!$('#edit-profile-container').is(':visible')){
            $("#view-profile-container").slideToggle(function(){ 
                $("#edit-profile-container").slideToggle()
            });
        }
    })

    // disable and enable new password
    $('#edit-user-form #new_password').prop("disabled",true)
    $('#edit-user-form #confirm_password').prop("disabled",true)
    $(document).on('input','#edit-user-form #current_password',function(){
        if($(this).val() != ''){
            $('#edit-user-form #new_password').prop("disabled",false)
        }else{
            $('#edit-user-form #new_password').prop("disabled",true)
            $('#edit-user-form #confirm_password').prop("disabled",true)
            $('#edit-user-form #new_password').val("")
            $('#edit-user-form #confirm_password').val("")
        }
    })

    $(document).on('input','#edit-user-form #new_password',function(){
        if($(this).val() != ''){
            $('#edit-user-form #confirm_password').prop("disabled",false)
        }else{
            $('#edit-user-form #confirm_password').val("")
            $('#edit-user-form #confirm_password').prop("disabled",true)
        }
    })

    // updating profile
    $(document).on('submit','#edit-user-form',function(e){
        e.preventDefault()

        const token = $("#edit-user-form [name='csrfmiddlewaretoken']").val()
        $.ajax({
            method:"POST",
            url: ACCOUNT_UPDATE,
            data:{
                'username': $('#edit-user-form #username').val(),
                'email': $('#edit-user-form #email').val(),
                'first_name': $('#edit-user-form #first_name').val(),
                'last_name': $('#edit-user-form #last_name').val(),
                'current_password': $('#edit-user-form #current_password').val(),
                'new_password': $('#edit-user-form #new_password').val(),
                'confirm_password': $('#edit-user-form #confirm_password').val()
            },
            headers:{
                'X-CSRFToken': token
            },
            dataType:'json',
            beforeSend : function(){
                $('#edit-user-form #submit').prop("disabled",true)
            },
            success:function(response){
                if(response.success){
                    toastr.options = {
                        "positionClass" : "toast-top-center",
                        "closeButton" : false,
                        "newestOnTop" : false,
                        "preventDuplicates" : false,
                        "timeOut" : "3000",
                        "progressBar": true
                    }
                    toastr.options.onHidden = ( 
                        ()=>{window.location.reload() }
                    )
                    toastr.success(response.message)
                    toastr.warning('Reloading the page')
                }else{
                    toastr.error("An error has occured. Please try again")
                }
                $('#edit-user-form #submit').prop("disabled",false)
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
                    $('#edit-user-form #submit').prop("disabled",false)
                }
            }
        })
    })
})
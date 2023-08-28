$(document).ready(function(){
    $(document).on('submit', '#add-contact-form', function(e){
        e.preventDefault();

        const token = $("#add-contact-form [name='csrfmiddlewaretoken']").val()
        $.ajax({
            method:"POST",
            url: CREATE_CONTACT,
            data:{
                'first_name': $('#first_name').val(),
                'last_name': $('#last_name').val(),
                'phone': $('#phone').val(),
                'company': $('#company').val(),
                'email': $('#email').val()
            },
            headers:{
                'X-CSRFToken': token
            },
            dataType:'json',
            success:function(response){
                if(response.success){
                    alert('contact created')
                }
            },
            error:function(response){
                const error = JSON.parse(response.responseText)
                alert(error.message)
            }
        })
    })
})
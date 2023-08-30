$(document).ready(function(){
    toastr.options = {
        "positionClass" : "toast-top-center",
        "closeButton" : false,
        "newestOnTop" : false,
        "preventDuplicates" : false,
        "timeOut" : "3000",
        "progressBar": true
    }
    const isJsonParsable = string => {
        let parsed = {}
        try {
            parsed = JSON.parse(string);
        } catch (e) {
            return false;
        }
        return parsed;
    }

    
    // view contacts
    function getContacts(){
        const table = $("#contact-list").DataTable({
            "lengthMenu": [ 5, 10, 20, 40, 50 ],
            'pageLength' : 5,
            'processing': true,
            'serverSide':true,
            'destroy': true,
            'draw':true,
            'ajax':{
                method: 'GET',
                url: VIEW_CONTACTS,
                async: false
            },
            columns: [
                {'data': 'id'},
                {'data': 'first_name'},
                {'data': 'last_name'},
                {'data': 'email'},
                {'data': 'company'},
                {'data': 'phone'},
                {'data': 'id', 'orderable': false, render: function(data, type, row){
                    const id = row.id
                    const first_name = row.first_name
                    const last_name = row.last_name
                    const email = row.email
                    const company = row.company
                    const phone = row.phone
                    return `<div
                        data-contact-id  = "${id}"
                        data-first-name = "${first_name}"
                        data-last-name = "${last_name}"
                        data-email = "${email}"
                        data-company = "${company}"
                        data-phone = "${phone}"
                        class="contact-details text-center"
                        >
                            <i class="material-icons ms-auto text-dark cursor-pointer" data-bs-toggle="tooltip" data-bs-placement="top" title="Edit" data-bs-original-title="Edit">edit</i>
                        </div>`;
                }},
            ],
            "language": {
                "paginate": {
                  "previous": '<span class="material-icons">arrow_back_ios</span>',
                  "next": '<span class="material-icons">arrow_forward_ios</span>'
                }
            },
            "responsive": true, "lengthChange": true, "autoWidth": false,
            "buttons": ["copy", "csv", "excel", "pdf", "print", "colvis"]
        }).buttons().container().appendTo('#contact-list_wrapper .col-md-6:eq(0)');
    }
    getContacts();

    // fill update contact form
    $(document).on('click','.contact-details',function(){
        $('#edit-contact-modal').modal('show')
        const contact_objects = $(this).map((index,element)=> $(element).data());
        const contact = Object.assign({}, ...contact_objects );

        const contact_id = contact.contactId
        const first_name = contact.firstName
        const last_name = contact.lastName
        const email = contact.email
        const company = contact.company
        const phone = contact.phone
    
        $('#update-contact-form  #update-contact-id').val(contact_id)
        $('#update-contact-form .first_name').val(first_name)
        $('#update-contact-form .last_name').val(last_name)
        $('#update-contact-form .email').val(email)
        $('#update-contact-form .company').val(company)
        $('#update-contact-form .phone').val(phone)
    })


    // add contact
    $(document).on('submit', '#add-contact-form', function(e){
        e.preventDefault();
        
        const token = $("#add-contact-form [name='csrfmiddlewaretoken']").val()
        $.ajax({
            method:"POST",
            url: CREATE_CONTACT,
            data:{
                'first_name': $('#add-contact-form .first_name').val(),
                'last_name': $('#add-contact-form .last_name').val(),
                'phone': $('#add-contact-form .phone').val(),
                'company': $('#add-contact-form .company').val(),
                'email': $('#add-contact-form .email').val()
            },
            headers:{
                'X-CSRFToken': token
            },
            dataType:'json',
            beforeSend:function(){
                $('#add-contact-form .submit').prop("disabled",true)
            },
            success:function(response){
                if(response.success){
                    toastr.success(response.message)
                    getContacts();
                }else{
                    toastr.error("An error has occured. Please try again")
                }
                $('#add-contact-form .submit').prop("disabled",false)
                $('#create-contact-modal').modal('hide')
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
                    $('#add-contact-form .submit').prop("disabled",false)
                }
            }
        })
    })

    // update contact
    $(document).on('submit', '#update-contact-form', function(e){
        e.preventDefault();
        
        const EDIT_CONTACT_URL = EDIT_CONTACT.replace('/0', `/${$('#update-contact-form #update-contact-id').val()}`)
        const token = $("#update-contact-form [name='csrfmiddlewaretoken']").val()

        $.ajax({
            method:'PUT',
            url: EDIT_CONTACT_URL,
            data:{
                'first_name': $('#update-contact-form .first_name').val(),
                'last_name': $('#update-contact-form .last_name').val(),
                'phone': $('#update-contact-form .phone').val(),
                'company': $('#update-contact-form .company').val(),
                'email': $('#update-contact-form .email').val()
            },
            dataType:'json',
            headers:{   
                'X-CSRFToken': token
            },
            beforeSend:function(){
                $('#update-contact-form .submit').prop("disabled",true)
            },
            success:function(response){
                if(response.success){
                    toastr.success(response.message)
                    getContacts();
                }else{
                    toastr.error("An error has occured. Please try again")
                }
                $('#update-contact-form .submit').prop("disabled",false)
                $('#edit-contact-modal').modal('hide')
            },
            error: function(response){
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
                    $('#update-contact-form .submit').prop("disabled",false)
                }
            }

        })
    })


})
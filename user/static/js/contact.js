$(document).ready(function(){

    // view contacts
    function getContacts(){
        $.ajax({
            method: 'GET',
            url: VIEW_CONTACTS,
            dataType:'json',
            beforeSend: ()=>{},
            success:(response)=>{
                const contacts = response.contacts;
                console.log(contacts)
                // show contacts table
                const contactsTable = contacts.map(
                    (contact) => 
                        `<tr class="contact-details">
                            <td data-contact-id  ="${contact.id}"> ${contact.id}</td>
                            <td data-first-name  ="${contact.first_name}"> ${contact.first_name} </td>
                            <td data-last-name   ="${contact.last_name}"> ${contact.last_name} </td>
                            <td data-email       ="${contact.email}"> ${contact.email} </td>
                            <td data-company     ="${contact.company}"> ${contact.company} </td>
                            <td data-phone       ="${contact.phone}"> ${contact.phone} </td>
                        </tr>`
                );
                $('#contact-list').children('tbody').html(()=>contactsTable)
            },
            error:()=>{
                alert('An Error Has Occured Setting Up Contact List');
            }
        })
    }
    getContacts();

    // fill update contact form
    $(document).on('click','.contact-details',function(){
        const contact_objects = $(this).children('td').map((index,element)=> $(element).data());
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
            success:function(response){
                if(response.success){
                    alert(response.message)
                }
            },
            error: function(response){
                const error = JSON.parse(response.responseText)
                alert(error.message)
            }

        })
    })


})
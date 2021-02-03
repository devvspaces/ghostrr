let toggle_nav = document.querySelector('#toggle_nav')
let nav = document.querySelector('#navigation')
let close_nav = document.querySelector('.close_nav')
try{
    toggle_nav.onclick = function (event) {
        if (nav.classList.contains('active')){
            nav.classList.remove('active')
        } else {
            nav.classList.add('active')
        }
    }
    close_nav.onclick = function (event) {
        nav.classList.remove('active')
    }
} catch(e){}


// Code to make close icon on alert messages delete messages
function deleteMessage(e){
	e.path.forEach(i=>{
		if (i.className=='close'){
			i.parentElement.remove()
			return
		}
	})
}
let alert_message = document.querySelectorAll('.alert')
try{
	alert_message.forEach(a=>{
		a.addEventListener('click', deleteMessage)
	})
} catch (e){

}


// Code to show and hide
let show_hint = document.querySelector('#show_hint')
let hint_section = document.querySelector('.hint_section')
let close_hint = document.querySelector('#close_hint')
try{
    show_hint.onclick = function (event) {
        if (hint_section.classList.contains('active')){
            hint_section.classList.remove('active')
        } else {
            hint_section.classList.add('active')
        }
    }
    close_hint.onclick = function (event) {
        hint_section.classList.remove('active')
    }
} catch(e){
    
}



// Code to edit and save profile 
let edit_profile = document.querySelector('#edit_profile')
let profile_box = document.querySelector('#profile_box')
let profile_box_inputs = document.querySelectorAll('#profile_box input')

try{
    edit_profile.onclick = function (event) {
        if (profile_box.classList.contains('view_mode')){
            profile_box.classList.remove('view_mode')
            edit_profile.innerHTML = "<i class='fas fa-times'></i>Discard"
            profile_box_inputs.forEach(i=>{
                i.removeAttribute('disabled')
            })
        } else {
            profile_box.classList.add('view_mode')
            edit_profile.innerHTML = "<i class='fas fa-pen'></i>Edit"
            profile_box_inputs.forEach(i=>{
                i.setAttribute('disabled','true')
            })
        }
    }
} catch(e){
    
}

// Codes for ajax setup for get and post requests to backend
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


let csrftoken = ''
try{
    csrftoken = getCookie('csrftoken');
} catch(e){}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}



try{
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});
} catch(e){
}


// Code to send post request containing btc amount to buy and sellbox pk with ajax
let generate_text = $('#generate_text')
let save_form = $('#save_form')
let first_form = $('#first_form')
let total_copy = $('#total_copy')
let loading = document.getElementById('loading')
let title = document.getElementById('title')
let sentence = document.getElementById('sentence')
let copy_length = document.getElementById('copy_length')
let text_content = document.querySelector('.text_content')
let title_form = document.getElementById('title_form')
let sentence_form = document.getElementById('sentence_form')
let copy_length_form = document.getElementById('copy_length_form')
let copy_text_form  = document.querySelector('#copy_text_form ')
let credit_data  = document.querySelector('#credit_data')
let radios = document.querySelectorAll(".radios input[name='copy_length'")
// let save_form = document.querySelectorAll('.save_form')


// save_form.forEach(i=>{
//     i.onclick = total_copy.submit()
// })

let retur = ''

function get_radio_selection(){
    radios.forEach(i=>{
        if(i.checked==true){
            retur = i.value
            return
        }
    })
}


total_copy.submit(function(event) {
    event.preventDefault()
    title_form.value = title.children[1].value
    sentence_form.value = sentence.children[1].value
    get_radio_selection()
    copy_length_form.value = retur
    console.log(get_radio_selection())
    copy_text_form.value = text_content.innerText

    this.submit()
})

first_form.submit(function(event) {
    loading.classList.add('active')
    event.preventDefault()
    let thisData = first_form.serialize()
    let thisURL = window.location.href // or set your own url
    $.ajax({
        method: "POST",
        url: thisURL,
        data: thisData,
        success: handleFormSuccess,
        error: handleFormError,
    })
})

try{
	generate_text.click(function(event){
        first_form.submit()
	})
} catch(e){
}

try{
	save_form.click(function(event){
        total_copy.submit()
	})
} catch(e){
}

function handleFormSuccess(data, textStatus, jqXHR){
    // console.log(data)
    // console.log(textStatus)
    // console.log(jqXHR)
    let text = data['text']

    // Check if text == 0
    if(data['error_message']){
        alert(data['error_message'])
    } else {
        text_content.innerText = text

        // Redude user credits
        credit_data.innerText = parseInt(credit_data.innerText)-1

        alert('Blog saved!')
    }

    
    loading.classList.remove('active')

    // Remove all erros in form
    title.removeAttribute('error')
    sentence.removeAttribute('error')
    copy_length.removeAttribute('error')

    // Setting all info in forms back to normal value
    title.lastElementChild.innerHTML = data['title']
    sentence.lastElementChild.innerHTML = data['sentence']
    copy_length.lastElementChild.innerHTML = data['copy_length']
}
let nons = 0
function handleFormError(jqXHR, textStatus){
    nons = jqXHR['responseJSON']
    let title_err = nons['errors']['title']
    let sentence_err = nons['errors']['sentence']
    let copy_length_err = nons['errors']['copy_length']
    if (title_err && title_err.length > 0){
        let title_text = ''
        title_err.forEach(i=>{
            title_text = title_text + i +'<br>'
        })
        title.lastElementChild.innerHTML = title_text
        title.setAttribute('error','True')
    } else {
        // Removing error and error text
        title.removeAttribute('error')
        title.lastElementChild.innerHTML = 'Enter the title you want for this blog here'
    }
    if (sentence_err && sentence_err.length > 0){
        let title_text = ''
        sentence_err.forEach(i=>{
            title_text = title_text + i +'<br>'
        })
        sentence.lastElementChild.innerHTML = title_text
        sentence.setAttribute('error','True')
    } else{
        sentence.removeAttribute('error')
        sentence.lastElementChild.innerHTML = 'Describe the blog you want to generate here'
    }
    if (copy_length_err && copy_length_err.length > 0){
        let title_text = ''
        copy_length_err.forEach(i=>{
            title_text = title_text + i +'<br>'
        })
        copy_length.lastElementChild.innerHTML = title_text
        copy_length.setAttribute('error','True')
    } else {
        copy_length.removeAttribute('error')
        copy_length.lastElementChild.innerHTML = 'Enter the length of copy you want'
    }
    // console.log(textStatus)
    loading.classList.remove('active')
}


// Code to select and copy text in create blog page
const copyToClipBoard = str => {
	const el = document.createElement('textarea')
	el.value = str
	el.setAttribute('readonly','')
	el.style.position = 'absolute'
	el.style.left = '-999px'
	document.body.appendChild(el)
	el.select()
	document.execCommand('copy')
	document.body.removeChild(el)
}
const copy_addy = document.querySelector('#copy_addy')
const addy = document.querySelector('.text_content')
try{
	copy_addy.onclick = function(event){
        event.preventDefault()
		copyToClipBoard(addy.innerText)
		this.innerText = 'Copied content'	}
} catch (e){
}


// Code to show delete modal in blog section
let delete_btn = document.querySelectorAll('.delete_btn')
let modal = document.querySelector('.modal')
let close_delete = document.querySelectorAll('.close_delete')
try{
    delete_btn.forEach(i=>{
        i.onclick = function(event){
            event.preventDefault()
    
            // Get link element on modal with class danger
            let delete_el = modal.querySelector('.danger')
            delete_el.href = this.getAttribute('deleteLink')
            
            modal.classList.add('active')
        }
    })
} catch(e){

}
try{
    modal.onclick = function (event) {
        if(event.target == modal){
            modal.classList.remove('active')
        }
    }
} catch(e){
    
}
try{
    close_delete.forEach(i=>{
        i.onclick = function(event){
            event.preventDefault()
            modal.classList.remove('active')
        }
    })
} catch(e){
    
}


// Code to delete a blog in edit mode
let delete_blog_in_edit = document.querySelector('#delete_blog_in_edit')
try{
    delete_blog_in_edit.onclick = function(event){
        event.preventDefault()
    
        // Get link element on modal with class danger
        let delete_el = modal.querySelector('.danger')
        delete_el.href = this.getAttribute('deleteLink')
        
        modal.classList.add('active')
    }
} catch(e){
    
}


// Get Stripe publishable key
if (payment_foo == 1){
    try{
        fetch("/payments/config/")
        .then((result) => { return result.json(); })
        .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);
        
        // new
        // Event handler
        let sumbitBtn = document.querySelector("#submitBtn")
        sumbitBtn.addEventListener("click", () => {
            // Show loader
            loading.classList.add('active')
    
            // Get Checkout Session ID
            fetch("/payments/create-checkout-session/")
            .then((result) => { return result.json(); })
            .then((data) => {
            console.log(data);
    
            // Redirect to Stripe Checkout
            return stripe.redirectToCheckout({sessionId: data.sessionId})
            })
            .then((res) => {
            console.log(res);
            });
        });
        });
    } catch(e){
    
    }
}


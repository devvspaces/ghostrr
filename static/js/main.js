let toggle_nav = document.querySelector('#toggle_nav')
let nav = document.querySelector('#navigation')
let close_nav = document.querySelector('.close_nav')
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


let csrftoken = getCookie('csrftoken');


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
	console.log(e)
}

// Code that gets data when generate is clicked on in the create blog page
let buyBitcoin = $('.buyBitcoin')

try{
	buyBitcoin.click(function(event){
		event.preventDefault()
		let sellbox_pk = event.target.parentElement.querySelector('.seller_pk').innerText
		let btc_amount_data = event.target.parentElement.parentElement.querySelector('.btc_amount_data').innerText
		// Create a string in serializable format and send with ajax
		let btcData = 'sellbox_pk='+sellbox_pk+'&btc_amount='+btc_amount_data
	    let thisURL = window.location.href // or set your own url
	    $.ajax({
	        method: "POST",
	        url: thisURL,
	        data: btcData,
	        success: handleRedirect,
	        error: handleFormError,
	    })
	})
} catch(e){
	console.log(e)
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
// let save_form = document.querySelectorAll('.save_form')


// save_form.forEach(i=>{
//     i.onclick = total_copy.submit()
// })


total_copy.submit(function(event) {
    event.preventDefault()
    title_form.value = title.children[1].value
    sentence_form.value = sentence.children[1].value
    copy_length_form.value = copy_length.children[1].value
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
	console.log(e)
}

try{
	save_form.click(function(event){
        total_copy.submit()
	})
} catch(e){
	console.log(e)
}

function handleFormSuccess(data, textStatus, jqXHR){
    // console.log(data)
    // console.log(textStatus)
    // console.log(jqXHR)
    let text = data['text']
    text_content.innerText = text

    // Redude user credits
    credit_data.innerText = parseInt(credit_data.innerText)-1
    loading.classList.remove('active')
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
        title.children[1].style.borderColor = 'red'
    }
    if (sentence_err && sentence_err.length > 0){
        let title_text = ''
        sentence_err.forEach(i=>{
            title_text = title_text + i +'<br>'
        })
        sentence.lastElementChild.innerHTML = title_text
        sentence.children[1].style.borderColor = 'red'
    }
    if (copy_length_err && copy_length_err.length > 0){
        let title_text = ''
        copy_length_err.forEach(i=>{
            title_text = title_text + i +'<br>'
        })
        copy_length.lastElementChild.innerHTML = title_text
        copy_length.children[1].style.borderColor = 'red'
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
	console.log(e)
}
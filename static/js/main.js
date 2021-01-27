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
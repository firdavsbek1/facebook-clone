let post_input=document.getElementById('message-sender')
let post_inputs=document.getElementsByClassName('messageSender__option')

post_input.addEventListener('click',function (event){

    window.location.href='http://localhost:8000/posts/'
})


post_array=Array.from(post_inputs)
post_array.forEach(function (item,index){
    item.addEventListener('click',function (event){
    window.location.href='http://localhost:8000/posts/'
})
})




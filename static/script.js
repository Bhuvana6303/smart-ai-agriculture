let chart;

// ---------------- SENSOR ---------------- //

function analyze(){

let m=parseInt(document.getElementById("moisture").value)
let t=parseInt(document.getElementById("temperature").value)

if(isNaN(m)||isNaN(t)){
alert("Enter values")
return
}

fetch("/recommendation",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({moisture:m,temperature:t})
})
.then(r=>r.json())
.then(d=>{

document.getElementById("result").innerHTML=d.result

let ctx=document.getElementById("chart")

if(chart) chart.destroy()

chart=new Chart(ctx,{
type:"bar",
data:{
labels:["Moisture","Temperature"],
datasets:[{
data:[m,t],
backgroundColor:["#22c55e","#3b82f6"]
}]
}
})

})
}

// ---------------- CHAT POPUP ---------------- //

function toggleChat(){
let popup=document.getElementById("chatPopup")

if(popup.style.display==="flex"){
popup.style.display="none"
}else{
popup.style.display="flex"
}
}

// ---------------- CHAT ---------------- //

function sendMessage(){

let input=document.getElementById("chatInput")
let msg=input.value.trim()

if(msg==="") return

let chat=document.getElementById("chatBox")

// show user message
chat.innerHTML+=`<div class="msg-user">${msg}</div>`

input.value=""

// typing animation
let typing=document.createElement("div")
typing.className="msg-bot"
typing.innerText="Typing..."
chat.appendChild(typing)

chat.scrollTop=chat.scrollHeight

fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:msg})
})
.then(res=>res.json())
.then(data=>{

typing.remove()

chat.innerHTML+=`<div class="msg-bot">${data.reply}</div>`

chat.scrollTop=chat.scrollHeight

})
.catch(err=>{
typing.remove()
chat.innerHTML+=`<div class="msg-bot">Error connecting to server</div>`
console.log(err)
})

}
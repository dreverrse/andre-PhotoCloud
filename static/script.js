function showImage(img){

const skeleton = img.parentElement.querySelector(".skeleton")

if(skeleton){
skeleton.remove()
}

img.classList.add("img-show")

}

/* =========================
   WAIT DOM READY
========================= */
document.addEventListener("DOMContentLoaded", function(){

const dropzone = document.getElementById("dropzone")
const progressBar = document.getElementById("progressBar")
const progressBox = document.getElementById("progressBox")

const viewer = document.getElementById("viewer")
const viewerImg = document.getElementById("viewerImg")

const uploadBtn = document.getElementById("uploadBtn")
const fileInput = document.getElementById("fileInput")

/* =========================
   IMAGE VIEWER
========================= */

window.openViewer = function(src){

viewerImg.src = src

viewer.style.display = "flex"

}

/* klik background = tutup */
viewer.addEventListener("click", function(){

viewer.style.display = "none"

})

/* klik gambar jangan menutup */
viewerImg.addEventListener("click", function(e){

e.stopPropagation()

})

/* =========================
   DRAG DROP
========================= */

dropzone.addEventListener("dragover", e=>{
e.preventDefault()
dropzone.classList.add("bg-gray-800")
})

dropzone.addEventListener("dragleave", ()=>{
dropzone.classList.remove("bg-gray-800")
})

dropzone.addEventListener("drop", e=>{
e.preventDefault()
dropzone.classList.remove("bg-gray-800")

let files = e.dataTransfer.files
uploadFiles(files)

})

dropzone.onclick = ()=>{
fileInput.click()
}

/* =========================
   UPLOAD FILE
========================= */

function uploadFiles(files){

for(let file of files){

let form = new FormData()
form.append("photo", file)

let xhr = new XMLHttpRequest()

xhr.open("POST","/upload")

progressBox.classList.remove("hidden")

xhr.upload.onprogress = function(e){

if(e.lengthComputable){

let percent = (e.loaded / e.total) * 100
progressBar.style.width = percent + "%"

}

}

xhr.onload = function(){

progressBar.style.width = "0%"
progressBox.classList.add("hidden")

location.reload()

}

xhr.send(form)

}

}

/* =========================
   DELETE PHOTO
========================= */

window.deletePhoto = function(name){

if(!confirm("Delete this photo?")) return

fetch("/delete/"+name)
.then(res=>{
if(res.ok){
location.reload()
}
})

}

/* =========================
   BUTTON UPLOAD
========================= */

uploadBtn.onclick = ()=>{
fileInput.click()
}

fileInput.addEventListener("change", function(){

let files = this.files
uploadFiles(files)

})

function updateTime(){

const now = new Date()

const time = now.toLocaleTimeString()
const date = now.toLocaleDateString()

document.getElementById("time").innerText = date + " • " + time

}

setInterval(updateTime,1000)
updateTime()

})

let photoToDelete = null

function openDeleteModal(name){

photoToDelete = name
document.getElementById("deleteModal").classList.remove("hidden")

}

function closeDeleteModal(){

document.getElementById("deleteModal").classList.add("hidden")

}

document.getElementById("confirmDelete").onclick = function(){

fetch("/delete/" + photoToDelete)
.then(res=>{
if(res.ok){
location.reload()
}
})

}

const toggle = document.getElementById("themeToggle")
const body = document.getElementById("appBody")

if(localStorage.getItem("theme") === "light"){
body.classList.remove("dark")
body.classList.add("light")
toggle.checked = true
}

toggle.addEventListener("change", ()=>{

if(toggle.checked){
body.classList.remove("dark")
body.classList.add("light")
localStorage.setItem("theme","light")
}else{
body.classList.remove("light")
body.classList.add("dark")
localStorage.setItem("theme","dark")
}

})

function toggleUploadMenu(){

const container = document.querySelector(".fab-container")

container.classList.toggle("active")

}
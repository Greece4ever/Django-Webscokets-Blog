/** Article Preview */ 

var __default__;

//for <script> and <... style=""> tags
const handleXXS = (value) => {
    const removed_script = value.replace(/<(\s+)?script/,'').replace(/<(\s+)?(\/)(\s+)?script/,'');
    const removed_style = removed_script.replace(/<(.*)(\s+)?style(\s+)?=('|")/g,'');
    return removed_style;
}

const title = document.getElementById("input_title");
const title_preview = document.getElementById("title");

const description = document.getElementById("post");
const description_preview = document.getElementById("description");

title.addEventListener("input",() => {
    title_preview.innerText = title.value; //title has no html
})

description.addEventListener("input",() => {
    description_preview.innerHTML = handleXXS(description.value) //handle XXS html tags
})

//For File uploading

const upload = document.getElementById("file_upload");
const imgres = document.getElementById("imgres");

const handleClick = (id) => {
    const elmnt = document.getElementById(id);
    __default__ = elmnt.getAttribute("id");
    elmnt.style.opacity = "0.4"
}


upload.addEventListener("input",(e) => {
    const files = e.target.files;
    document.getElementById("file_num").textContent = files.length;
    document.getElementById("thumbnail").src = URL.createObjectURL(files[0]);
    document.getElementById("thumbnail_chose").style.visibility = "visible";
    const thumbnails = document.getElementById("thumbnails");
    Array.from(files).forEach(file => {
        thumbnails.innerHTML += `<img id="${file.filename}" onclick="handleClick(${file.filename})" data-toggle="tooltip" data-placement="right" title="${file.name}" class="img-thumbnail" src="${URL.createObjectURL(file)}"></div><br><br>`
    })

})


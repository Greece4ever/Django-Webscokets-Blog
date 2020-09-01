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
    let x = "\n<p>" + handleXXS(description.value);
    x = x + "\n";
    x = x.replace(/[\n]+/g,"\n</p><p>");
    description_preview.innerHTML = x //handle XXS html tags
})

//For File uploading

const upload = document.getElementById("file_upload");
const imgres = document.getElementById("imgres");

const handleClick = (id) => {
    const elmnt = document.getElementById(id);
    document.querySelectorAll(".selected").forEach(item => {
        item.classList.remove("selected")
    })

    __default__ = elmnt.getAttribute("title");
    document.getElementById("thumnail_chosen_name").textContent = __default__;

    elmnt.classList.add("selected");
}


upload.addEventListener("input",(e) => {
    console.log("called");
    const files = e.target.files;
    document.getElementById("file_num").textContent = files.length;
    document.getElementById("thumbnail").src = URL.createObjectURL(files[0]);
    document.getElementById("thumbnail_chose").style.visibility = "visible";
    const thumbnails = document.getElementById("thumbnails");
    let i = 0;
    let hashes = [];
    thumbnails.innerHTML = ''; //Get rid of the previous ones
    console.log(thumbnails.innerHTML)
    Array.from(files).forEach(file => {
        name = Math.random() * Math.random() * Math.random() * 255;
        name = String(name);
        thumbnails.innerHTML += `<img id="${name}" data-toggle="tooltip" data-placement="right" title="${file.name}" class="img-thumbnail" src="${URL.createObjectURL(file)}"></div><br><br>`
        hashes.push(name);
        i++;
    })
    console.log(hashes);
    let C = 0;
    hashes.forEach(id => {
        if (C == 0) {
            let x = document.getElementById(id);
            __default__ = x.getAttribute("title");
            x.classList.add("selected");
            document.getElementById("thumnail_chosen_name").textContent = x.getAttribute("title");
        }
        document.getElementById(id).addEventListener("click",() => {
            handleClick(id);
        })
        C++;
    })


})


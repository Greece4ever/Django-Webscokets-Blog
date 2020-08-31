/** Article Preview */ 

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
    console.log(description_preview.innerHTML.length)
    description_preview.innerHTML = handleXXS(description.value) //handle XXS html tags
})


document.getElementById("imgres").addEventListener("dragover",(e) => {
    console.log(e)
    e.preventDefault();
})

const upload = document.getElementById("file_upload");
const imgres = document.getElementById("imgres");

upload.addEventListener("input",(e) => {
    const files = e.target.files;
    console.log(files)
    let rnd;
    document.getElementById("thumbnail").src = URL.createObjectURL(files[0])
})

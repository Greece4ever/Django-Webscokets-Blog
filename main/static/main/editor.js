//For html help in text

const textarea = document.getElementById("post");

const insertAtStringButDoNotRemove = (str,index,value) => {
    return str.substring(0,index) + value + str.substring(index)
}

document.querySelectorAll(".html").forEach(element => {
    element.addEventListener("click",(e) => {
        let end = textarea.selectionEnd;
        let html_tag = e.currentTarget.id;
        console.log(html_tag)
        textarea.focus();
        console.log(`Cursor : ${textarea.selectionStart}`)
        textarea.value = insertAtStringButDoNotRemove(textarea.value,textarea.selectionStart,`<${html_tag}>\t</${html_tag}>`) 
        textarea.selectionEnd = end+(html_tag.length+3)
    })
})

// First create the file via Ajax and if the response is Positive
// It will give the id of the article
// which in turn will be send in the websocket
// and it will be appended to everyone connected

var __id__;

const confirm_submit = document.getElementById("create_article");

const create_article = (formData,csrf_token) => {
    return axios.post("",formData,{
        headers : {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken' : csrf_token
        }
    })
}

confirm_submit.addEventListener("click",function(e){
    const title = document.getElementById("input_title").value;
    let description = document.getElementById("post").value;
    let x = "\n<p>" + description
    x = description + "\n"
    console.log(x.replace(/[\n]+/g,"\n</p><p>"))
    description = x;
    const files = document.getElementById("file_upload").files;

    if(title.length < 1 || description.length < 20 || files.length === 0)
    {
        //Minumun requirements
        const error = document.getElementById("error");
        error.innerHTML = `
        One of the following requirements was <b>ignored</b>:
        <li>Description must be <b>more than 20</b> characters</li>
        <li>Title must be <b>more than 1</b> character</li>
        <li>Article must contain <b>at least one</b> image</li>

        `
        error.style.visibility = "visible";
        error.style.position = "relative";
        return -1;
    }

    const csrf_token = document.querySelector("input[name]").value;
    console.log(csrf_token);

    let formData = new FormData();
    formData.append("title",title); //title
    formData.append("description",description); //body
    formData.append("thumbnail",__default__);
    let C = 0;
    Array.from(files).forEach((file) => {
        formData.append(`file_${C}`,file);
        C++
    })

    const createArticle = async () => {
        const response = await create_article(formData,csrf_token);
        console.log(response)
        if(response.data.error) 
        {
            error.style.visibility = "visible";
            error.style.position = "relative";
            error.innerText = response.data.error;
            return null;
        }
        let id = response.data.id;
        __id__ = id;
        const socket = new WebSocket("ws://" + window.location.host + "/ws/articles/"); //Connect with the socket

    }
    createArticle();
})

socket.onopen = () => {
    socket.send(id).then(() => {
        location.href = "/articles/" + title.replace(/\s+/g,"-") + `-${id}/`;
    })

}; //Send the id of the post

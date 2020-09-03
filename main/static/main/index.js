//Home-Page-Websockets
const handleXXS = (value) => { //for XXS
    const removed_script = value.replace(/<(\s+)?script/,'').replace(/<(\s+)?(\/)(\s+)?script/,'&lt;script');
    const removed_style = removed_script.replace(/<(.*)(\s+)?style(\s+)?=('|")/g,'');
    return removed_style;
}

var __articles__;


const socket = new WebSocket(`ws://${window.location.host}/ws/articles/`);

const queryArticle = (article_array) => {
    return axios.get("auth/articles/view",{
        headers : {
            "articles" : [
                JSON.stringify(article_array)
            ]
        }
    })
}

//Likes and dislikes
document.querySelectorAll('.bi.bi-hand-thumbs-up').forEach(element => {
    // console.log(element)
    element.addEventListener("click",function(e) {
        let data = {
            type : "vote",
            article_id : e.currentTarget.id.replace("img_","")
        }
        console.log(e.target.id)
        console.log(data)
        socket.send(JSON.stringify(data));
    })
})

const appendArticle = (response) => {
    response.forEach(article => {
        innerHTML = `
        <div style="margin-top : 20px;" class="container article">
            ${article.date_created} <span style="margin-left : 5px" class="badge badge-secondary">New</span></h1>
            <div style="float: right;">
                <img style="width: 32px;border-radius: 64px;" src="${article.img_user}">
            </div>
            <hr>
            <div style="float: left;margin: 10px;" style="position: relative;" class="image">
                <a id="img_${article.id}" href="#"><img id="img_${article.id}__" class="external" style="width: 400px;" src="${article.image}"></a>
            </div>
            <label class="name_pictuire" style="margin-top : 10px;position: relative;cursor: pointer;"><a id="nam${article.id}" href="${'articles/' + article.name.replace(/\s+/g,'-') + '-' +  article.id}" style="color: #333;text-decoration: none;"></a>                
                <span class="like_count" style="float: right;"><b id="likes_${article.id}">${article.likes}</b>
                <svg id="img_${article.id}" style="margin-bottom: 3px;" width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-hand-thumbs-up" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a9.84 9.84 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733.058.119.103.242.138.363.077.27.113.567.113.856 0 .289-.036.586-.113.856-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.163 3.163 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16v-1c.563 0 .901-.272 1.066-.56a.865.865 0 0 0 .121-.416c0-.12-.035-.165-.04-.17l-.354-.354.353-.354c.202-.201.407-.511.505-.804.104-.312.043-.441-.005-.488l-.353-.354.353-.354c.043-.042.105-.14.154-.315.048-.167.075-.37.075-.581 0-.211-.027-.414-.075-.581-.05-.174-.111-.273-.154-.315L12.793 9l.353-.354c.353-.352.373-.713.267-1.02-.122-.35-.396-.593-.571-.652-.653-.217-1.447-.224-2.11-.164a8.907 8.907 0 0 0-1.094.171l-.014.003-.003.001a.5.5 0 0 1-.595-.643 8.34 8.34 0 0 0 .145-4.726c-.03-.111-.128-.215-.288-.255l-.262-.065c-.306-.077-.642.156-.667.518-.075 1.082-.239 2.15-.482 2.85-.174.502-.603 1.268-1.238 1.977-.637.712-1.519 1.41-2.614 1.708-.394.108-.62.396-.62.65v4.002c0 .26.22.515.553.55 1.293.137 1.936.53 2.491.868l.04.025c.27.164.495.296.776.393.277.095.63.163 1.14.163h3.5v1H8c-.605 0-1.07-.081-1.466-.218a4.82 4.82 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"/>
                </svg>    
            </span>
            </label>
            <p id="description_${article.id}" style="font-size: 15px;text-align: justify;" class="lead text-muted">{${handleXXS(article.description)}}</p>
        </div>
        <br>
        <br>
        `
        const target = document.getElementById("innerArticles");
        target.innerHTML = innerHTML + target.innerHTML;
        document.getElementById(`nam${article.id}`).innerText = article.name;
    })
}

async function getArticle() {
    const resposne = await queryArticle([12]);
    appendArticle(resposne.data.success);
}

document.getElementById("new_posts").addEventListener("click",() => {
    getArticle();
})

//Receiving data
socket.onmessage = function(message) {
    let data = JSON.parse(message.data);
    console.log(data)
    if (data.type == "vote")
    {
        console.log(data)
        console.log("Changing likes")
        console.log(document.getElementById(`likes_${data.id}`))
        document.getElementById(`likes_${data.id}`).innerHTML = data.likes
    }
    else { //post
        console.log("Pushing data")
        __articles__.push(data.id);
    }
}

//Home-Page-Websockets

const socket = new WebSocket(`ws://${window.location.host}/ws/articles/`);

//Likes and dislikes
document.querySelectorAll('.bi.bi-hand-thumbs-up').forEach(element => {
    // console.log(element)
    element.addEventListener("click",function(e) {
        let target = e.target;
        let data = {
            type : "vote",
            article_id : e.target.id.replace("img_","")
        }
        console.log(e.target.id)
        console.log(data)
        socket.send(JSON.stringify(data));
    })
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
}

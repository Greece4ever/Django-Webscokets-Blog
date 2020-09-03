const handleXXS = (value) => {
    return value.replace(/<(\s+)?script/,'').replace(/<(\s+)?(\/)(\s+)?script/,'')
}

const len = (args) => {
    return args.length;
}

const href = window.location.href.split('-');
const target = `ws://${window.location.host}/ws/posts/${href[href.length-1]}`;
const socket = new WebSocket(target);

//For making comments

try {
    document.getElementById("comment").addEventListener("focus",() => {
        document.getElementById("buttons").style.visibility = "visible";
    })

    document.getElementById("cancel").addEventListener("click",() => {
        document.getElementById("comment").blur()
        document.getElementById("buttons").style.visibility = "hidden";
    })

    document.getElementById("post").addEventListener("click",function() {
        console.log("click")
        const message = document.getElementById("comment").value;
        const data = {
            type : "comment",
            data : message,
            is_reply : false
        }
        socket.send(JSON.stringify(data))
        })
}
catch {}

//Adding ability to comment

const addCommentEvent = (element) => {
    element.addEventListener("click",(e) => {
        const id = e.target.id.replace("reply",'');
        console.log(id)
        document.getElementById("reply_" + id).innerHTML = `
        <div style="margin-top : 30px" class="media">
        <img style="width: 72px;margin-top: 5px;border-radius: 50px;" class="mr-3" src="/media/{{user.userprofile.profile_image}}" alt="Generic placeholder image">
        <div class="media-body">
          <textarea id="reply__${id}" style="margin-top: 10px;resize: none;" placeholder="${e.target.textContent}" class="form-control"></textarea>
          <div id="das" style="float: right;margin-top: 10px;">
            <button onclick="handleReply(${id})" style="background-color: #333;color: #fff;margin-right: 10px;" class="btn btn primary">Post</button>
            <button onclick="document.getElementById('reply_${id}').innerHTML = ''" style="background-color: #6d0d0d;color: #fff;"  class="btn btn danger">Cancel</button>
          </div>
        </div>
      </div>`
    })

}


socket.onmessage = (message) => {
    console.log("Received message");
    message = JSON.parse(message.data);
    const hash = Math.random().toString();
    let marginLeft = message.is_reply ? "100px" : "" 
    let html = `
    <div style="margin-top: 50px;margin-left : ${marginLeft}" class="media">
        <img style="width: 72px;margin-top: 5px;border-radius: 50px;" class="mr-3" src="${message.img}" alt="Generic placeholder image">
        <div class="media-body">
            <h5 id="nam_${hash}" class="mt-0">                </h5>
            <span class="badge badge-secondary">New</span>
            <p class="lead">
                ${handleXXS(message.msg)}
            </p>
            <a id="reply{{comment.pk}}" class="reply" style="color: #007bff;">Reply to <i id="r_${hash}"></i></a>
            <span style="float: right;" class="text-muted">${message.date_created}</span>
            <div class="reply" id="reply_${message.id}"></div>
        </div>
      </div>  
    `;
    if (message.is_reply)
    {
        document.getElementById(`replies_${message.parent_id}`).innerHTML = html + document.getElementById(`replies_${message.parent_id}`).innerHTML;
    } else {
        document.getElementById('comments_detail').innerHTML = html + document.getElementById('comments_detail').innerHTML;
    }
    document.getElementById(`nam_${hash}`).textContent = message.name;
    document.getElementById(`r_${hash}`).textContent = message.name;
    addCommentEvent(document.getElementById(`reply_${message.id}`))
}

const handleReply = (parent_id) => {
    console.log("Handling reply")
    const data = {
        type : "comment",
        data : document.getElementById(`reply__${parent_id}`).value,
        parent : parent_id,
        is_reply : true
    }
    console.log(data)
    socket.send(JSON.stringify(data));
}

document.querySelectorAll(".reply").forEach(element => {
    element.addEventListener("click",(e) => {
        const id = e.target.id.replace("reply",'');
        console.log(id)
        document.getElementById("reply_" + id).innerHTML = `
        <div style="margin-top : 30px" class="media">
        <img style="width: 72px;margin-top: 5px;border-radius: 50px;" class="mr-3" src="/media/{{user.userprofile.profile_image}}" alt="Generic placeholder image">
        <div class="media-body">
          <textarea id="reply__${id}" style="margin-top: 10px;resize: none;" placeholder="${e.target.textContent}" class="form-control"></textarea>
          <div id="das" style="float: right;margin-top: 10px;">
            <button onclick="handleReply(${id})" style="background-color: #333;color: #fff;margin-right: 10px;" class="btn btn primary">Post</button>
            <button onclick="document.getElementById('reply_${id}').innerHTML = ''" style="background-color: #6d0d0d;color: #fff;"  class="btn btn danger">Cancel</button>
          </div>
        </div>
      </div>`
    })
})

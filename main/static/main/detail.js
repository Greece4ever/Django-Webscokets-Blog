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

    document
    
    document.querySelectorAll(".com_rate").forEach(rate => {
        rate.addEventListener('click',() => {
            let id = rate.id.replace(/[a-zZ-a]+/g,'');
            let vote = rate.id.includes("dislike") ? "dislike" : "like"
            let specific = "comment";
            let data = {
                type : "vote",
                data : "com_rate",
                id : id,
                vote : vote,
                specific: specific
            }
            console.log(data)
            socket.send(JSON.stringify(data));
        })        
    })
    
    document.getElementById("likes").addEventListener('click',() => {
        const data = {
            data : "art_like",
            type : "rate",
            vote :  "like",
            specific : "article",
        }
        console.log(data)
        socket.send(JSON.stringify(data));

    })
    
    document.getElementById("dislikes").addEventListener('click',() => {
        const data = {
            data : "art_dis",
            type : "rate",
            vote :  "dislike",
            specific : "article",
        }
        console.log(data)
        socket.send(JSON.stringify(data));

    })
}
catch {
    console.error("User Authentication Failed aborting socket connection")
}

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

const updateArticleRating = (num_like,num_dislike) => {
    document.getElementById("denmaresei").innerText = num_dislike;
    document.getElementById("mouaresei").innerText = num_like;
}

const updateCommentRating = (id,num_like,num_dislike,) => {
    document.getElementById("com_like_" + id + "_69").textContent = num_like;
    document.getElementById("com_dislike_" + id + "_69").textContent = num_like;
}



socket.onmessage = (message) => {
    message = JSON.parse(message.data);
    console.log(message)
    if (message.type == 'vote')
    {
        if (message.specific == 'comment')
        {
            updateCommentRating(`${message.id}`,message.likes,message.dislikes)
        }
        else {
            updateArticleRating(message.likes,message.dislikes)
        }
        return -1;

    }
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

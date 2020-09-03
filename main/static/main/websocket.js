// First create the file via Ajax and if the response is Positive
// It will give the id of the article
// which in turn will be send in the websocket
// and it will be appended to everyone connected
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
        const socket = await new WebSocket("ws://" + window.location.host + "/ws/articles/"); //Connect with the socket
        socket.send(id); //Send the id of the post
        location.href = "/articles/" + title.replace(/\s+/g,"-") + `-${id}/`;

    }
    createArticle();

})


// <p>Είναι πλέον κοινά παραδεκτό ότι ένας αναγνώστης αποσπάται από το περιεχόμενο που διαβάζει, όταν εξετάζει τη διαμόρφωση μίας σελίδας.</p> Η ουσία της χρήσης του Lorem Ipsum είναι ότι έχει λίγο-πολύ μία ομαλή κατανομή γραμμάτων, αντίθετα με το να βάλει κανείς κείμενο όπως 'Εδώ θα μπει κείμενο, εδώ θα μπει κείμενο', κάνοντάς το να φαίνεται σαν κανονικό κείμενο. <p>Πολλά λογισμικά πακέτα ηλεκτρονικής σελιδοποίησης και επεξεργαστές ιστότοπων πλέον χρησιμοποιούν το Lorem Ipsum σαν προκαθορισμένο δείγμα κειμένου, και η αναζήτησ για τις λέξεις 'lorem ipsum' στο διαδίκτυο θα αποκαλύψει πολλά web site που βρίσκονται στο στάδιο της δημιουργίας. </p>Διάφορες εκδοχές έχουν προκύψει με το πέρασμα των χρόνων, άλλες φορές κατά λάθος, άλλες φορές σκόπιμα (με σκοπό το χιούμορ και άλλα συναφή).
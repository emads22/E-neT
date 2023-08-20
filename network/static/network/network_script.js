document.addEventListener("DOMContentLoaded", function() {
    handle_post_editing();
    handle_post_reaction();
})


function handle_post_editing() {
    // catch all edit post links
    const post_links = document.querySelectorAll(".edit-link");
    post_links.forEach(post_link => {
        post_link.addEventListener("click", () => {
            // extract post ID from the link ID (its 'editLink_{ID}')
            const post_id = post_link.id.split("_")[1]; 
            // navigate to the post content
            const post_content = document.getElementById(`post_${post_id}`);
            
            edit_post(post_id, post_content);
        })
    })
}


function edit_post(post_id, post_content) {
    
    const content_textarea = document.getElementById(`post_${post_id}_edit`);
    const save_btn = document.getElementById(`save_btn_${post_id}`);
    const modal = document.getElementById(`editModal_${post_id}`);   
    // must include CSRF token in fetch request headers below (CSRF protection). This is essential for any non-GET requests to Django views.
    // so access this data attribute to retrieve CSRF token without relying on searching DOM and avoid catching everytime initial token only 
    const csrf_token = save_btn.getAttribute('data-csrf');
    // set the base url to use it in fetch by accessing "http://127.0.0.1:8000" using "window.location.origin"
    const base_url = window.location.origin;
    // populate the textarea with old content
    content_textarea.value = post_content.textContent;
    // on change (user types in the textarea)
    content_textarea.addEventListener("change", function() {
        // populate/update the textarea with new content that is the latest input value ('this' is event.target here which is the textarea)
        content_textarea.value = this.value;
    })

    save_btn.addEventListener("click", () => {       
        // construct the URL to avoid concatenating urls and getting errors specially when switching between several pages
        const url = `${base_url}/posts/edit/${post_id}`;
        // make the PUT request to server
        fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,
            },
            body: JSON.stringify({
                content: content_textarea.value,
            }),
        })
        .then(response => response.json())
        .then(result => {
            // print result on console
            console.log(result);
            // populate the post wth the new content if its existant
            if (result["edited_content"]) {
                post_content.textContent = result["edited_content"]; 
            }            
            // get the instance of the modal to close it in js without using 'data-bs-dismiss="modal"' on save button in template
            const modalInstance = bootstrap.Modal.getInstance(modal);
            modalInstance.hide();    // close the modal
            // display message on webpage
            load_temp_message(post_id, result["message"]);
        })
        .catch(error => {
            // display caught error on console
            console.log(error);
            // display message on webpage
            load_temp_message(post_id, result["message"]);
        })
    })
}


function handle_post_reaction() {
    // catch all like buttons
    const post_like_btns = document.querySelectorAll(".btn-like");
    post_like_btns.forEach(like_btn => {
        like_btn.addEventListener("click", () => {
            // extract post ID from the like button ID (its 'postReaction_{ID}')
            const post_id = like_btn.id.split("_")[1]; 
            post_reaction(post_id);
        })
    })
}


function post_reaction(post_id) {
    const likes = document.getElementById(`postLikes_${post_id}`);
    // construct the URL 
    const url = `${window.location.origin}/posts/${post_id}/reaction`;
    // make the GET request to server
    fetch(url)
    .then(response => response.json())
    .then(result => {
        // print result on console
        console.log(result);
        // populate likes wth the new value
        likes.innerText = result["total_likes"];
        // display message on webpage
        load_temp_message(post_id, result["message"]);
    })
    // display caught error
    .catch(error => {
        console.log(error);
        // display message on webpage
        load_temp_message(post_id, result["message"]);
    })
}


function load_temp_message(post_id, message) {
    // navigate to message element
    const message_element = document.getElementById(`message_post_${post_id}`);
    message_element.innerHTML = `${message[0]} - ${message[1]}`;
    // after 2 seconds clear the message
    setTimeout(function() {
        message_element.innerHTML = "";
    }, 2000);  // execute after 2 second (2000 ms)
}
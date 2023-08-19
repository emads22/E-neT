document.addEventListener("DOMContentLoaded", function() {
    handle_post_editing();
    handle_post_liking();
})


function handle_post_editing() {
    // catch all posts with edit option
    const post_links = document.querySelectorAll(".edit-link");
    post_links.forEach(post_link => {
        post_link.addEventListener("click", () => {
            // extract post ID from the link ID (its 'editLink_{ID}')
            const post_id = post_link.id.split("_")[1]; 
            edit_post(post_id);
        })
    })
}


function edit_post(post_id) {
    const post_content = document.getElementById(`post_${post_id}`);
    const content_textarea = document.getElementById(`post_${post_id}_edit`);
    const save_btn = document.getElementById(`save_btn_${post_id}`);
    const modal = document.getElementById(`editModal_${post_id}`);   
    // populate the textarea with old content
    content_textarea.value = post_content.textContent;
    // declare this variable here to be accessible in this scope not only below under (like global var)
    let new_content = "";
    // on change
    content_textarea.addEventListener("change", function() {
        // update new_content with latest input value ('this' is event.target here which is the textarea)
        new_content = this.value;
    })

    save_btn.addEventListener("click", () => {
        // populate the post wth the new content
        post_content.textContent = new_content;
        // must include the CSRF token in fetch request headers (CSRF protection). This is essential for any non-GET requests to Django views.
        // so access this data attribute to retrieve CSRF token without relying on searching DOM and avoid catching everytime initial token only 
        const csrfToken = save_btn.getAttribute('data-csrf');
        // set the base url by accessing "http://127.0.0.1:8000" using "window.location.origin"
        const base_url = window.location.origin;
        // construct the URL to avoid concatenating urls and getting errors specially when switching between several pages
        const url = `${base_url}/posts/edit/${post_id}`;
        // make the PUT request to server
        fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                content: new_content,
            }),
        })
        .then(response => response.json())
        .then(result => {
            // print result on console
            console.log(result);
                        
            // get the instance of the modal to close it in js without using 'data-bs-dismiss="modal"' on save button in template
            const modalInstance = bootstrap.Modal.getInstance(modal);
            modalInstance.hide();    // close the modal
        })
        // display caught error
        .catch(error => console.log(error));
    })
}


function handle_post_liking() {
    // catch all posts with edit option
    const post_like_btns = document.querySelectorAll(".btn-like");
    post_like_btns.forEach(like_btn => {
        like_btn.addEventListener("click", () => {
            // get the reaction of the like button (data-reaction attribute) and toggle between its states
            let reaction = (like_btn.getAttribute('data-reaction') === "unlike") ? "like" : "unlike";
            like_btn.setAttribute("data-reaction", reaction);
            // extract post ID from the like button ID (its 'postReaction_{ID}')
            const post_id = like_btn.id.split("_")[1]; 
            // access this data attribute to retrieve CSRF token
            const csrfToken = like_btn.getAttribute('data-csrf');
            post_reaction(post_id, reaction, csrfToken);
            // console.log(like_btn.getAttribute('data-reaction'));
        })
    })
}


function post_reaction(post_id, the_reaction, csrf_token) {
    const likes = document.getElementById(`postLikes_${post_id}`);
    let updated_likes;
    if (the_reaction === 'like') {
        updated_likes = parseInt(likes.innerText) + 1;
    } else {
        updated_likes = parseInt(likes.innerText) - 1;
    }
    // populate likes wth the new value
    likes.innerText = updated_likes;
    // construct the URL 
    const url = `${window.location.origin}/posts/${post_id}/reaction`;
    // make the PUT request to server
    fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            reaction: the_reaction,
        }),
    })
    .then(response => response.json())
    .then(result => {
        // print result on console
        console.log(result);
    })
    // display caught error
    .catch(error => console.log(error));
}
document.addEventListener("DOMContentLoaded", function() {
    handle_post_editing();
})


function handle_post_editing() {
    // catch all posts with edit option
    const post_links = document.querySelectorAll(".edit-link");
    post_links.forEach(post_link => {
        // console.log(post_link.id, post_link.textContent);
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
        // must include the CSRF token in fetch request headers (CSRF protection). This is essential for any non-GET requests to Django views.
        // so access this data attribute to retrieve CSRF token without relying on searching DOM and avoid catching everytime initial token only 
        const csrfToken = save_btn.getAttribute('data-csrf');
        // set the base url
        const base_url = "http://127.0.0.1:8000";
        // construct the URL to avoid concatenating urls and getting errors specially when switching between several pages
        const url = `${base_url}/posts/edit/${post_id}`;

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
            // populate the post new content from result of response
            post_content.textContent = result["new_content"];
            // get the instance of the modal to close it in js without using 'data-bs-dismiss="modal"' on save button in template
            const modalInstance = bootstrap.Modal.getInstance(modal);
            modalInstance.hide();    // close the modal
        })
        // display caught error
        .catch(error => console.log(error));
    })
}
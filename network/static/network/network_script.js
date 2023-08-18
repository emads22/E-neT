document.addEventListener("DOMContentLoaded", function() {
    edit_post();
})


function edit_post() {

    const text_box = document.createElement("textarea");
    text_box.id = "post-content-edit";
    text_box.className = "list-inline-item";
    const save_btn = document.createElement("button");
    save_btn.className = "btn btn-primary list-inline-item";    
    save_btn.id = "save-btn";
    save_btn.textContent = "Save";

    const edit_link = document.querySelector(".edit-link");
    edit_link.onclick = (event) => {
        // prevent the default behavior of <a> to not scroll to top page (or redirect somewhere)
        event.preventDefault(); 
        // navigate to parent of the 'edit' link (<p>)
        const p_section = event.target.parentElement;
        // get the first child of this parent <p> which is the <span> that holds the post content
        const post_content = p_section.firstElementChild;

        console.log(post_content);

        // add the post content text to the new textarea value where the edit is happening
        text_box.value = post_content.textContent;
        // insert the new elements ('text_box' and 'save_btn') before the first child 'post_content'
        p_section.insertBefore(save_btn, post_content);
        p_section.insertBefore(text_box, post_content);
        // p_section.insertBefore(save_btn, post_content);
        // .insertAdjacentElement("beforebegin", text_box);
        p_section.insertAdjacentElement("beforebegin", save_btn);
        post_content.style.display = "none";
        event.target.style.display = "none";

        save_btn.onclick = update_post(post_content);
        
    }
}



function update_post(content_element) {
    content_element.textContent = "HELLO";
    // content_element.style.display = "block";
}
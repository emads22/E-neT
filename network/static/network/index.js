document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    // document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    // document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    // document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    // document.querySelector('#create').addEventListener('click', create_post);
  
    // By default, load the inbox
    load_posts();

    // add a post
    document.querySelector('#create-form').addEventListener('submit', add_post);
  });


function show_section(this_section) {
    // create a list of sections ids
    const sections = ['#posts-view', '#create-view', '#post-content-view', '#temp-message'];
    // for each section if its same as section prameter passed then show this section otherwise hide all the rest
    sections.forEach(section => {
        if (section === this_section) {
            document.querySelector(section).style.display = 'block';
        } else {
            if (section === '#temp-message') {
                const temp_message = document.querySelector(section);
                // if the temp message is success ('email sent successfully') then keep it shown (it will automatically be hidden afterwards)
                temp_message.style.display = temp_message.textContent.includes('Error:') ? 'none': 'block';
            } else {
                document.querySelector(section).style.display = 'none';
            }            
        }
    })
}


function load_posts() {
    // Clear out post content field
    document.querySelector('#create-content').value = '';
}


function add_post(event) {
    // Prevent the default form submission behavior
    event.preventDefault(); 
    // Scroll to the top of the window (to show temp message if success or failure instead of staying at bottom of page)
    // window.scrollTo(0, 0);
    // send email data using POST method to server
    fetch('/posts/create', {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector('#create-content').value
        })
    })
    .then(response => {
        // in case of server error the fetch connection is still successful but the error inside the data handling logic in the server 
        // (error of status other than 200 like 400 or else ) so throw a new error and get the message sent from the view function.
        if (!response.ok) {
            return response.json().then(result => {
                // display result (error) on console as JSON dict
                console.log(result);
                // throw new error to catch it in '.catch()' and pass the result error message sent as JSON under key 'error'
                throw new Error(result.error);
              })
        } else {
            // if response is ok so all successful then return response in JSON format
            return response.json(); 
        }
    })
    .then(result => {
        // display successful result on console as JSON dict
        console.log(result);
        load_temp_message(result, true);
        // load the user’s posts after sending the email
        load_posts();
    }) 
    .catch(error => load_temp_message(error, false));
}



//   function create_post() {

//     // Show create view and hide other views
//     document.querySelector('#emails-view').style.display = 'none';
//     document.querySelector('#create-view').style.display = 'block';
  
//     // Clear out composition fields
//     document.querySelector('#create-recipients').value = '';
//     document.querySelector('#create-subject').value = '';
//     document.querySelector('#create-body').value = '';
//   }


function load_posts() {
  
//     // Show the mailbox and hide other views
//     document.querySelector('#emails-view').style.display = 'block';
//     document.querySelector('#create-view').style.display = 'none';
  
    // Show the posts
    document.querySelector('#posts-view').innerHTML = `<h3>Hello World. These are all the posts.</h3>`;
}


function load_temp_message(response_result, success) {

    const temp_message = document.querySelector('#temp-message');
    temp_message.style.display = 'block';
    // in response returned, the key is 'message'. if success is true then show it in green otherwise its false so show error in red
    if (success) {
        temp_message.innerHTML = `<div class="alert alert-success fs-5" role="alert">${response_result.message}</div>`;
    }
    else {
        temp_message.innerHTML = `<div class="alert alert-danger fs-5" role="alert"><strong>Error: </strong>${response_result.message}</div>`;
    }
    // if the result message was a success or a server error then display it temporary
    if (!response_result.message.includes('Failed to fetch')) {
        // setTimeout(callback, delay) is a built-in JS function that allows us to schedule execution of a function after a specified delay 
        // in milliseconds. so here after showing success temp msg for 3 seconds hide it back
        setTimeout(() => {
            temp_message.style.display = 'none';
            temp_message.innerHTML = '';
        }, 3000);
    } else {
        // otherwise theres no response and its a fetch error so add some text to temp message and hide everything else on page
        document.querySelector(".alert-danger").append(' requested data.');
        // show '#temp-message' div only  
        show_section('#temp-message');
    }
}

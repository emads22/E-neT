# E:neT Social Network App

## Overview:
E:neT is a Twitter-like social network website for making posts and following users. This application was developed as part of my [**CS50W Fourth Project**](https://cs50.harvard.edu/web/2020/) in 2023. You can explore its development on [me/50](https://github.com/me50/emads22/tree/web50/projects/2020/x/network) repository.

---

## Features

1. **New Post**
   - Users can create new text-based posts by entering text in a textarea and submitting.

2. **All Posts**
   - Displays all posts from all users.
   - Shows username, post content, post date/time, and number of likes.
   - Posts are sorted with the most recent first.

3. **Profile Page**
   - Clicking on a username loads that user’s profile page.
   - Displays follower and following counts.
   - Shows all user posts in reverse chronological order.
   - Includes a "Follow" or "Unfollow" button for other users.

4. **Following Page**
   - Shows posts from users that the current user follows.
   - Pagination with 10 posts per page.
   - Only accessible to signed-in users.

5. **Pagination**
   - Posts displayed with pagination.
   - "Next" and "Previous" buttons to navigate between pages of posts.

6. **Edit Post**
   - Users can edit their own posts.
   - Click "Edit" on their posts to modify content using a textarea.
   - Save changes without reloading the entire page using JavaScript.

7. **Like and Unlike**
   - Users can like/unlike posts.
   - Asynchronously updates like count without page reload using JavaScript.

---

## Setup
1. Clone the repository.
2. Ensure Python 3.x is installed.
3. Install dependencies with `pip install -r requirements.txt`.
4. Configure database settings in `settings.py`.
5. Run Django development server: `python manage.py runserver`.

## Usage
1. Access the web app through your browser at `http://127.0.0.1:8000/`.
2. Register for an account or log in to start using the social networking features.
3. Create posts, follow users, like posts, and explore other functionalities.

## Example
#### Sami's User Profile:
- **Username**: `sami`
- **Password**: `123456` 

Sami actively participates in E:neT, creating insightful posts and engaging with other users' content. He uses the platform to connect with like-minded individuals and share his thoughts on various topics.

## Contributing
Contributions are welcome! Here are ways to contribute:
- Report bugs or issues.
- Suggest new features or improvements.
- Submit pull requests with enhancements.

## Author
- Emad &nbsp; E>
  
  [<img src="https://img.shields.io/badge/GitHub-Profile-blue?logo=github" width="150">](https://github.com/emads22)

## License
This project is licensed under the MIT License, which grants permission for free use, modification, distribution, and sublicense of the code, provided that the copyright notice (attributed to [emads22](https://github.com/emads22)) and permission notice are included in all copies or substantial portions of the software. This license is permissive and allows users to utilize the code for both commercial and non-commercial purposes.

Please see the [LICENSE](LICENSE) file for more details.

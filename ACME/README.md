# ACME - CS50 Final Project

#### My Youtube Video:
https://youtu.be/ECpfQ5Yh2Wc

### Overview:
This web-based cybersecurity challenge was developed using Python (Flask), HTML/CSS (Bootstrap), and SQLite.

At first glance, the website appears to be a fully functional company website that provides comprehensive information about the company, services they provide, and contact details. It includes an admin dashboard that offers detailed insights into the current customer base, including their packages and service duration.

The website has been intentionally designed to be susceptible to security vulnerabilities. The design gives the user an interactive environment where they can acquire knowledge, conduct thorough exploration, and exploit these vulnerabilities in a controlled manner.

This project, which was developed for my Harvard CS50 final project, showcases a comprehensive understanding of web development, database usage, cybersecurity principles, and user experience design.

### Features
- **Realistic login portal with vulnerabilities:**\
Includes a working login form designed to simulate real-word vulnerabilities such as SQL injection allowing users to bypass authentication.

- **Real-time mission progress tracking:**\
Challenges are tracked in real-time, with progress saved and displayed through interactive UI elements and backend logic.

- **Multiple different types of hacking:**\
Not all challenges require code based hacking, I wanted to demonstrate to users that it is important to take care when designing the layout of your site. If the site is not laid out correctly, you could become vulnerable to being hacked. I also wanted to demonstrate user error which can cause your site to be hacked.

- **Interactive UI feedback:**\
Toast notifications, modals, pop-overs and conditional animations provide immediate feedback when users trigger or complete objectives.

- **Caught Counter:**\
Users run the risk of being "caught" during form submissions or suspicious actions. These are tracked and displayed as part of the overall mission.

- **Backend challenge validation:**\
Python/flask backend verifies whether a challenge was completed legitimately before updating the user's score or display congratulation modals.

- **Mission control dashboard:**\
A dedicated modal window which is accesable at all times in the bottom right of the users screen
reveals the users current mission, the amount of times the user has been caught, hints, answers, and also allows the user to reset and start from scratch.

- **Fully responsive design:**\
Built using Bootstrap 5 for a clean and responsive layout across all screen sizes


### Project Goals
I created this project to build an interactive web application that safely simulates real-world web security vulnerabilities. My goal was to design a hands-on learning platform where users can explore and understand the impact of common security flaws, such as SQL injection, session manipulation, and access control issues. Beyond its role as a challenge-based environment, the site also functions as a fully operational business website—highlighting how even professional looking platforms can harbor serious vulnerabilities beneath the surface. By combining engaging challenges with modern frontend design and robust backend logic, I aimed to create an immersive experience that not only demonstrates my technical skills but also encourages greater awareness of secure web development practices.

### User Journey
1. **Landing page**
Upon arrival at the business landing page, users are greeted by a welcome modal. This modal introduces the site, outlines the challenges ahead, and sets the tone for the experience. Once dismissed, users are presented with what appears to be a standard company homepage. However, their first objective is hidden in plain sight: locate the concealed employee login page.

2. **Login page**
After discovering the hidden login route, users are met with a congratulatory modal acknowledging their progress and providing insight into how such a flaw could be mitigated in real-world applications. Upon closing the modal, users encounter a login form styled to resemble an internal employee portal. A sticky note on the page reveals a username and a tea-stained password, hinting at insecure information handling. The user must now bypass authentication and gain access to the admin account

3. **Admin Dashboard**
Successfully breaching the admin credentials unlocks another modal. This time offering sample code and best practices to prevent SQL injection attacks. Once dismissed, users find themselves on the admin dashboard, simulating privileged access within a business system. Here, they must complete their next mission: defacing the website using tools available to the administrator. This stage encourages users to consider the impact of poor access control and backend logic flaws.

4. **Easter egg**
After defacing the site, users are challenged with one final objective: discover the hidden easter egg. This secret element is embedded within the site and requires careful inspection and creative thinking to uncover. Completing this last task marks the full completion of all missions and triggers a final celebratory modal to recognize the user’s achievement.

### Key Technologies Used
- **Flask (Python):** For backend framework used for building route handling, user session logic, and database interaction.

- **SQlite:** Simple database used to store user state, customer data, and challenge progress.

- **HTML/CSS (Bootstrap):** Used for responsive layout and styling.

- **JavaScript:** Handles communications between frontend and backend for live updates.


### Final Thoughts
This project aims to balance technical depth with playful interaction, using humour and immersion to teach critical cybersecurity principles.
While the site is designed to be broken, it still functions as a legitimate company site, with working pages, animations, layout, and user flows. That dual-purpose design is intentional — to show how real-world websites might seem secure while still hiding exploitable flaws.

### How to run
1. Clone the repository
2. Install dependencies: **pip install -r requirements.txt**
3. Run **Flask run**
4. Open https://localhost:5000 in your browser
5. Begin the challenge


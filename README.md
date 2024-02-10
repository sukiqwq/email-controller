# email controller
## Introduction

This project aims to enable remote control functionalities via email. It allows users to remotely execute specific tasks by simply sending an email. This solution is particularly useful for scenarios that do not require real-time operations, such as downloading resources or logging into games to claim rewards.

## Team Members

- Ruqing Liu - UGA
- Wei Liang - UGA

## Project Goal

To provide a remote control functionality using email, enabling users to remotely execute predefined operations or run Python scripts through email. This process simplifies remote control, making it not only convenient but also extensible.

## Tools Used

- PyCharm: For Python code development.
- GitHub: For code version control and collaboration.
- Other Python Libraries: `json`, `os`, `smtplib`, `subprocess`, `time`, `imbox`, `pystray`, `PIL`, `tkinter`.

## Functionality

- **Initialization**: Reads configuration files, sets up email address and password information.
- **Email Handling**: Logs into the email server, monitors unread emails, filters legitimate emails, and executes preset operations.
- **User Interface**: Provides a graphical interface for users to input IMAP and SMTP server information, email addresses, and passwords, along with a system tray icon for easy management of the program's running state.

## Challenges and Solutions

Throughout the development of the project, we encountered several challenges:

1. **Environment Configuration**: We wanted users to be able to use the software directly, avoiding the hassle of configuring the running environment. We addressed this by simplifying the installation process and providing detailed installation guides.
2. **Security**: The need to securely store user passwords. We plan to implement a more secure password storage mechanism.
3. **Extensibility and Convenience**: Maintaining the software's extensibility while providing convenience to users. We achieved this by offering templates and example scripts, and simplifying the script invocation process.

## Achievements and Learnings

- Successfully built the platform and provided users with example templates.
- Learned how to call `subprocess` and `rpc`, as well as how to control a remote computer to execute tasks via email.

## Future Plans

- In the short term, improve the security of password storage, add software update reminders, and log on the server side.
- Long-term goals include developing a user-friendly mobile app, providing more control methods (such as Telegram bot, Discord bot), and allowing users to write run codes in a simpler way.


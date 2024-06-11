# cyChore
This is a python script that aims to ease out the process of assign and notify tasks team members in a weekly basis, serving more like a template rather than a library, specially if the tasks rotate every week. 

This project was designed to be a small, easy to scale, highly-customizable, out-of-the-box, you name it, solution that requires minimum set-up to start sending notifications and reminders.

Even thought it is a well rounded script it stills need to be run by the user, you my want to consider tools like Windows Task Scheduler, Zapier, webhooks, etc.

# How to use
1. Clone the repo.
2. Open "config.ini".
    - Configure the [smtp parameters](https://docs.python.org/3/library/smtplib.html).
    - Configure an starting date in YYYY-MM-DD format.
    - Modify/Add html templates.
3. Modify/Add your own users.json.
4. Add tasks to the tasks buffer.
5. Run the script

# Users
The default user type follows these structure:
- name
- personal_email
- initial task position (relative to the buffer task)
``` json
{
    "name": [
        "email@domain.com",
        0
    ]
}
```

# Customization
As previously mentioned the focus of this project is to serve like a template rather than library, using high-level functions rather than low-level abstractions, allowing you to start using it out-of-the-box.
Some potential improvements and customizations include:
- Implementing ifferent assignment logic
- Integrating databases for user information retrieval.
- Adding custom email templates.

# Default Template
![image](https://github.com/AlexGarc-sudo/cyChore/assets/144295305/737d3dcd-f997-4b57-bc99-82a51a595f11)

## Contributing

Guidelines for contributing to this project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## Contact
Alex Garcia - [alexgarciat00@gmail.com](mailto:alexgarciat00@gmail.com)

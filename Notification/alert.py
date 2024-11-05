from mailersend import emails

mailer = emails.NewEmail("mlsn.12adcdc2cb52e1c4d6831fdfa698e22a84d79b9c8e8214826fd09195aaaaa2b9")

# define an empty dict to populate with mail values
mail_body = {}

mail_from = {
    "name": "Home Security System",
    "email": "rasppi39@gmail.com",
}

recipients = [
    {
        "name": "Sakari",
        "email": "sakari.heinio@gmail.com",
    }
]


mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Alert!", mail_body)
mailer.set_html_content("You have been burgled!", mail_body)
mailer.set_plaintext_content("We detected movement in your home, calling the police is suggested.", mail_body)

# using print() will also return status code and data
mailer.send(mail_body)



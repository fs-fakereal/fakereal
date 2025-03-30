// // using Twilio SendGrid's v3 Node.js Library
// // https://github.com/sendgrid/sendgrid-nodejs
// javascript
// const sgMail = require('@sendgrid/mail')
// sgMail.setApiKey(process.env.SENDGRID_API_KEY)
// const msg = {
//   to: 'test@example.com', // Change to your recipient
//   from: 'test@example.com', // Change to your verified sender
//   subject: 'Sending with SendGrid is Fun',
//   text: 'and easy to do anywhere, even with Node.js',
//   html: '<strong>and easy to do anywhere, even with Node.js</strong>',
// }
// sgMail
//   .send(msg)
//   .then(() => {
//     console.log('Email sent')
//   })
//   .catch((error) => {
//     console.error(error)
//   })

require("dotenv").config();

// check that the api key is there
// console.log(process.env.SENDGRID_API_KEY);

const sendGridMail = require("@sendgrid/mail");
sendGridMail.setApiKey(process.env.SENDGRID_API_KEY);

const message = {
    to: "maukarletizia@gmail.com",
    from: "fakere.41@gmail.com",
    subject: "Test",
    // text: "test test sent",
    html: "<strong>FakeReal</strong>",
};

sendGridMail
    .send(message)
    .then(() => {
        console.log('Email was sent successfully!');
    })
    .catch((error) => {
        console.log(error);
    })
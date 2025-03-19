const express = require('express');
const bodyParser = require('body-parser');
const nodemailer = require('nodemailer');
const path = require('path');
require('dotenv').config(); // Load environment variables from .env

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware to parse JSON and URL-encoded form data
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files (CSS, JS, images)
app.use(express.static(path.join(__dirname)));

// Route to handle form submissions
app.post('/contact', (req, res) => {
    const { name, email, message } = req.body;

    // Validate the input
    if (!name || !email || !message) {
        return res.status(400).json({ error: 'All fields are required' });
    }

    // Send email using Nodemailer
    const transporter = nodemailer.createTransport({
        service: 'gmail', // Use your email service
        auth: {
            user: process.env.EMAIL_USER, // Your email (from .env)
            pass: process.env.EMAIL_PASS // Your email password (from .env)
        }
    });

    const mailOptions = {
        from: email, // Sender's email
        to: process.env.EMAIL_USER, // Your email (from .env)
        subject: `New Contact Form Submission from ${name}`,
        text: `Name: ${name}\nEmail: ${email}\nMessage: ${message}`
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.error('Error sending email:', error);
            return res.status(500).json({ error: 'Error sending email' });
        } else {
            console.log('Email sent:', info.response);
            return res.status(200).json({ message: 'Message sent successfully' });
        }
    });
});

// Route to handle signup form submissions
app.post('/signup', (req, res) => {
    const { name, email, password } = req.body;

    // Validate the input
    if (!name || !email || !password) {
        return res.status(400).json({ error: 'All fields are required' });
    }

    // Here you would typically save the user to a database
    console.log('User signed up:', { name, email, password });

    return res.status(200).json({ message: 'Signup successful' });
});

// Route to handle login form submissions
app.post('/login', (req, res) => {
    const { email, password } = req.body;

    // Validate the input
    if (!email || !password) {
        return res.status(400).json({ error: 'All fields are required' });
    }

    // Here you would typically check the user's credentials against a database
    console.log('User logged in:', { email, password });

    return res.status(200).json({ message: 'Login successful' });
});

// Serve the HTML files
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/about', (req, res) => {
    res.sendFile(path.join(__dirname, 'about.html'));
});

app.get('/contact', (req, res) => {
    res.sendFile(path.join(__dirname, 'contact.html'));
});

app.get('/allergy', (req, res) => {
    res.sendFile(path.join(__dirname, 'allergy.html'));
});

app.get('/upload', (req, res) => {
    res.sendFile(path.join(__dirname, 'uploadDNAimage.html'));
});

app.get('/signup', (req, res) => {
    res.sendFile(path.join(__dirname, 'signup.html'));
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'login.html'));
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
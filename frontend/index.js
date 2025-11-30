const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3000;
const FLASK_API_URL = process.env.FLASK_API_URL || 'http://backend:5000';
// const FLASK_API_URL = 'http://127.0.0.1:5000';
// const FLASK_API_URL = 'http://3.109.210.69:5000'; // for same instance deployment
// const FLASK_API_URL = 'http://13.233.163.245:5000'; // for same instance deployment
app.use(bodyParser.json());
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'form.html'));
});

app.post('/submit-form', async (req, res) => {
    try {
        const todo = req.body;
        const response = await axios.post(`${FLASK_API_URL}/process`, { 
            item_name: todo.title,
            item_description: todo.description
         });
        console.log("Flask backend response", response.data);

        res.json({
            success: true,
            data: response.data,
            message: 'Form submitted successfully'
        });
    } catch (error) {
        console.error('Error communicating with Flask API:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.listen(PORT, () => {
    console.log(`Frontend server is running on http://localhost:${PORT}`);
    console.log(`Flask API is running on ${FLASK_API_URL}`);
});
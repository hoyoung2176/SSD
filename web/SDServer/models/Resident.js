const mongoose = require('mongoose');

const ResidentSchema = new mongoose.Schema({
    name: String,
    age: Number,
    photo: String,
});

module.exports = mongoose.model('Resident',ResidentSchema);
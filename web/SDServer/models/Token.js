const mongoose = require('mongoose');

const TokenSchema = new mongoose.Schema({
    code: String,
});

module.exports = mongoose.model('Token',TokenSchema);
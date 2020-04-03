const mongoose = require("mongoose");

let questionsSchema = new mongoose.Schema({
  qid: {
    type: String,
    require: true
  },
  questions: {
    type: [],
    require: false
  },
  answers: {
    require: false
  }
});

module.exports = mongoose.model("Questionss", questionsSchema);

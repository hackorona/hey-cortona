const mongoose = require("mongoose");

// The object we should thake from the server
let questionsSchema = new mongoose.Schema(
  {
    qid: {
      type: String,
      require: true,
    },
    questions: {
      type: [],
      require: true,
    },
    answers: {
      type: [],
      require: true,
      default: [],
    },
  },
  { minimize: false }
);

module.exports = mongoose.model("question", questionsSchema);

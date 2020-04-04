const mongoose = require("mongoose");

let questionsSchema = new mongoose.Schema(
  {
    qid: {
      type: String,
    },
    questions: {
      type: [],
      require: false,
    },
    answers: {
      type: Object,
      require: true,
      default: {},
    },
  },
  { minimize: false }
);

module.exports = mongoose.model("question", questionsSchema);

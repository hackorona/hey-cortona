const express = require("express");
const router = express.Router();
const Questions = require("../models/Questions");

router.get("/", async (req, res) => {
  try {
    const questions = await Questions.find();
    res.json(questions);
  } catch (err) {
    res.json(err);
  }
});

router.post("/", async (req, res) => {
  const questions = new Questions(req.body);
  try {
    const savedQuestions = await questions.save();
    res.json(savedQuestions);
  } catch (err) {
    console.log(err);
    res.json(err);
  }
});

router.patch("/:qid", async (req, res) => {
  try {
    const questionUpdate = await Questions.updateOne(
      { qid: req.params.qid },
      { $set: { questions: req.body.questions } }
    );
    res.json(questionUpdate);
  } catch (err) {
    res.json(err);
  }
});
module.exports = router;

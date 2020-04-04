const express = require("express");
const router = express.Router();
const questions = require("../models/questions");

router.get("/", async (req, res) => {
  try {
    const questions_arr = await questions.find();
    res.json(questions_arr);
  } catch (err) {
    res.json(err);
  }
});

router.post("/", async (req, res) => {
  const questions_obj = new questions(req.body);
  try {
    const savedQuestions = await questions_obj.save();
    res.json(savedQuestions);
  } catch (err) {
    console.log(err);
    res.json(err);
  }
});

router.patch("/", async (req, res) => {
  try {
    const questionUpdate = await questions.updateOne(
      { qid: req.body.qid },
      { $set: { questions: req.body.questions } }
    );
    res.json(questionUpdate);
  } catch (err) {
    res.json(err);
  }
});
module.exports = router;

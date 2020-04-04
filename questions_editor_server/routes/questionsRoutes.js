const express = require("express");
const router = express.Router();
const questions = require("../models/questions");

// Get all the Questions from the server
router.get("/", async (req, res) => {
  try {
    const questions_arr = await questions.find();
    res.json(questions_arr);
  } catch (err) {
    res.json(err);
  }
});

// Delete a specific Questions from the server
router.delete("/", async (req, res) => {
  try {
    const removedQuestions = await questions.remove({ qid: req.body.qid });
    res.json(removedQuestions);
  } catch (err) {
    res.json(err);
  }
});

// Add new Questions
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

// Update an existing Questions
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

// The routes
module.exports = router;

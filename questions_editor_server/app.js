const express = require("express");
const mongoose = require("mongoose");
require("dotenv/config");
const app = express();
const bodyParse = require("body-parser");
const cors = require("cors");
const questionsRoute = require("./routes/questionsRoute");

app.use(cors());

app.use(bodyParse.json());
app.use("/questions", questionsRoute);

mongoose.connect(process.env.DB_CONNECTION, { useNewUrlParser: true }, () =>
  console.log("connected to db")
);

app.listen(4000);

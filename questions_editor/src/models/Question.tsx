export default class Question {
  question: string = "";
  isChecked = false;
  constructor(question: string) {
    this.question = question;
  }
}

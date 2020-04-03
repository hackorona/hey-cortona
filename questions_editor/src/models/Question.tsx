export default class Questions {
  qid: string = "";
  question: string = "";
  isChecked = false;
  constructor(qid: string, question: string) {
    this.qid = qid;
    this.question = question;
  }
}

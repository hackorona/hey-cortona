import { observable, IObservableArray, action } from "mobx";
import Questions from "../models/Questions";
import Question from "../models/Question";
import axios from "axios";

class QuestionsStore {
  @observable questions: IObservableArray<Questions> = observable([]);
  public async getInitialData() {
    const tempData = await axios.get("http://localhost:4000/questions");
    this.questions.replace(tempData.data);
  }

  public async addQuestions(questions: Questions) {
    await axios.post("http://localhost:4000/questions", questions);
  }

  public async moveQueestions(questions: Questions) {
    await axios.patch(
      "http://localhost:4000/questions/" + questions.qid,
      questions.questions
    );
  }

  public findQuestionsById(qid: string) {
    return this.questions.find((item: Questions) => {
      return item.qid === qid;
    });
  }

  @action
  public markQuestion(qid: string, index: number) {
    const questions = this.findQuestionsById(qid);
    if (questions) {
      questions.questions[index].isChecked = !questions.questions[index]
        .isChecked;
    }
  }

  public createNewCategory(qid: string) {
    const newCategory: Questions = new Questions();
    newCategory.qid = qid;
    this.questions.push(newCategory);
  }

  @action
  public moveMarked(qid: string) {
    const tempMarked: Question[] = [];
    let target = this.questions[0];
    let remove: number[] = [];

    this.questions.forEach((items: Questions) => {
      remove = [];
      if (items.qid === qid) {
        target = items;
      }
      items.questions.forEach((item, index) => {
        if (item.isChecked) {
          item.isChecked = false;
          tempMarked.push(item);
          remove.push(index);
        }
      });
      for (let i = 0; i < remove.length; i++) {
        items.questions.splice(remove[i] - i, 1);
      }
    });

    tempMarked.forEach(item => {
      item.qid = target.qid;
      target.questions.push(item);
    });

    this.questions.replace(
      this.questions.map(items => {
        if (qid === items.qid) {
          return target;
        }
        return items;
      })
    );
  }
}

const questionsStore = new QuestionsStore();
export default questionsStore;

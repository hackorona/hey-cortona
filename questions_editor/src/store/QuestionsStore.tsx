import { observable, IObservableArray, action, toJS } from "mobx";
import Questions from "../models/Questions";
import Question from "../models/Question";
import axios from "axios";

class QuestionsStore {
  @observable questions: IObservableArray<Questions> = observable([]);
  public async getInitialData() {
    const tempData = await axios.get("http://localhost:4000/questions");
    this.questions.replace(this.convertQuestions(tempData.data));
  }

  // Convert the info from the database to my objects
  public convertQuestions(tempData: any) {
    tempData.forEach((element: any) => {
      element.questions.forEach((question: string, index: number) => {
        element.questions[index] = new Question(question);
      });
    });
    return tempData;
  }

  // Convert my objects to the database one's
  public convertFromQuestions(updateArray: any) {
    const temp = toJS(this.questions);
    updateArray.forEach((offset: number) => {
      temp[offset].questions.forEach((question: any, index: number) => {
        temp[offset].questions[index] = question.question;
      });
    });
    return temp;
  }

  public isExist(qid: string) {
    return this.questions.find((questions: Questions) => {
      return questions.qid === qid;
    });
  }

  public convertFromOneQuestions(element: any) {
    element.questions.forEach((question: Question, index: number) => {
      element.questions[index] = question.question;
    });

    return element;
  }

  public async addQuestions(questions: Questions) {
    await axios.post("http://localhost:4000/questions", questions);
    await this.getInitialData();
  }

  public async deleteQuestions(qid: string) {
    await axios.delete("http://localhost:4000/questions/", {
      data: {
        qid: qid,
      },
    });
    await this.getInitialData();
  }

  public async updateQuestions(questions: any) {
    return await axios.patch("http://localhost:4000/questions/", {
      questions: questions.questions,
      qid: questions.qid,
    });
  }

  public async moveQuestions(updateArray: number[]) {
    const tempData = this.convertFromQuestions(updateArray);
    updateArray.forEach(async (place: any) => {
      const questions = tempData[place];
      if (questions.questions.length > 0) {
        this.updateQuestions(questions);
      } else {
        this.deleteQuestions(questions.qid);
      }
    });
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
    newCategory.questions = [new Question(qid)];
    this.addQuestions(this.convertFromOneQuestions(newCategory));
  }

  public deleteMarked() {
    let shouldUpdateCheck = false;
    const shouldUpdate: number[] = [];
    let remove: number[] = [];
    this.questions.forEach((items: Questions, offset: number) => {
      shouldUpdateCheck = false;
      remove = [];
      items.questions.forEach((item: Question, index) => {
        if (item.isChecked) {
          shouldUpdateCheck = true;
          remove.push(index);
        }
      });
      if (shouldUpdateCheck) {
        shouldUpdate.push(offset);
      }
      for (let i = 0; i < remove.length; i++) {
        items.questions.splice(remove[i] - i, 1);
      }
    });

    this.moveQuestions(shouldUpdate);
  }

  @action
  public async moveMarked(qid: string) {
    const tempMarked: Question[] = [];
    let target = this.questions[0];
    let remove: number[] = [];
    const shouldUpdate: number[] = [];
    let shouldUpdateCheck = false;

    this.questions.forEach((items: Questions, offset: number) => {
      remove = [];
      if (items.qid === qid) {
        target = items;
      }
      shouldUpdateCheck = false;
      items.questions.forEach((item: Question, index) => {
        if (item.isChecked) {
          item.isChecked = false;
          tempMarked.push(item);
          remove.push(index);
          shouldUpdateCheck = true;
        }
      });
      if (shouldUpdateCheck) {
        shouldUpdate.push(offset);
      }
      for (let i = 0; i < remove.length; i++) {
        items.questions.splice(remove[i] - i, 1);
      }
    });

    tempMarked.forEach((item) => {
      target.questions.push(item);
    });
    this.questions.map((items: Questions, index: number) => {
      if (qid === items.qid) {
        shouldUpdate.push(index);
        return target;
      }
      return items;
    });
    this.moveQuestions(shouldUpdate);
  }
}

const questionsStore = new QuestionsStore();
export default questionsStore;

import { observable, IObservableArray, action } from "mobx";
import Questions from "../models/Questions";
import Question from "../models/Question";

class QuestionsStore {
  @observable questions: IObservableArray<Questions> = observable([]);
  public getInitialData() {
    const tempData = [];
    tempData.push(new Questions());
    tempData.push(new Questions());
    tempData[0].qid = "0";
    tempData[0].questions = [
      new Question("0", "aaa?"),
      new Question("0", "asdasdasdasd?")
    ];
    tempData[1].qid = "1";
    tempData[1].questions = [
      new Question("1", "כמה זמן צריך להישאר בבידוד?"),
      new Question("1", "מי הבן אדם הכי מסכן בבידוד?")
    ];
    tempData.push(new Questions());
    tempData.push(new Questions());
    tempData[2].qid = "2";
    tempData[2].questions = [
      new Question("2", "aaa?"),
      new Question("2", "asdasdasdasd?")
    ];
    tempData[3].qid = "3";
    tempData[3].questions = [
      new Question("3", "כמה זמן צריך להישאר בבידוד?"),
      new Question("3", "מי הבן אדם הכי מסכן בבידוד?")
    ];
    tempData.push(new Questions());
    tempData.push(new Questions());
    tempData[4].qid = "4";
    tempData[4].questions = [
      new Question("4", "aaa?"),
      new Question("4", "asdasdasdasd?")
    ];
    tempData[5].qid = "5";
    tempData[5].questions = [
      new Question("5", "כמה זמן צריך להישאר בבידוד?"),
      new Question("5", "מי הבן אדם הכי מסכן בבידוד?")
    ];

    this.questions.replace(tempData);
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
    this.questions.forEach((items: Questions, index) => {
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

    for (let i = 0; i < this.questions.length; i++) {
      if (this.questions[i].questions.length === 0) {
        this.questions.splice(i, 1);
        i--;
      }
    }
  }
}

const questionsStore = new QuestionsStore();
export default questionsStore;

import React, { Component } from "react";
import { observer } from "mobx-react";
import "semantic-ui-css/semantic.min.css";
import { Card, Button } from "semantic-ui-react";
import questionsStore from "../store/QuestionsStore";
import Questions from "../models/Questions";
import Question from "../models/Question";

interface IProps {
  qid: string;
}
interface IState {
  reRender: boolean;
}
@observer
class QuestionCard extends Component<IProps, IState> {
  constructor(props: Readonly<IProps>) {
    super(props);
    this.state = {
      reRender: false
    };
  }

  render() {
    const info: Questions | undefined = questionsStore.findQuestionsById(
      this.props.qid
    );
    return (
      info && (
        <Card>
          <Card.Content>
            <Card.Header>{info.qid} </Card.Header>
          </Card.Content>
          {info.questions.map((question: Question, index: number) => {
            return (
              <Card.Content
                className={
                  info.questions[index].isChecked ? "checked" : undefined
                }
                key={question.question + index + question.qid}
                onClick={() => {
                  questionsStore.markQuestion(info.qid, index);
                  this.setState({ reRender: !this.state.reRender });
                }}
              >
                {question.question}
              </Card.Content>
            );
          })}
          <Card.Content>
            <Button
              color="red"
              onClick={() => {
                questionsStore.moveMarked(this.props.qid);
                this.setState({ reRender: false });
              }}
            >
              Move Marked Here
            </Button>
          </Card.Content>
        </Card>
      )
    );
  }
}

export default QuestionCard;

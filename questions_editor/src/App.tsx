import React, { Component } from "react";
import { observer } from "mobx-react";
import "semantic-ui-css/semantic.min.css";
import { Header, Grid } from "semantic-ui-react";
import "./App.scss";
import questionsStore from "./store/QuestionsStore";
import Questions from "./models/Questions";
import QuestionCard from "./components/QuestionCard";

interface IProps {}

interface IState {}

@observer
class App extends Component<IProps, IState> {
  constructor(props: Readonly<IProps>) {
    super(props);
    this.state = {};
    questionsStore.getInitialData();
  }

  render() {
    return (
      <div className="my-title">
        <Header className="my-header" size="huge">
          Corona Editor
        </Header>
        <Grid centered className="cards">
          {questionsStore.questions.map((item: Questions) => {
            return <QuestionCard key={item.qid} qid={item.qid}></QuestionCard>;
          })}
        </Grid>
      </div>
    );
  }
}

export default App;

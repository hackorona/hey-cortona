import React, { Component } from "react";
import { observer } from "mobx-react";
import "semantic-ui-css/semantic.min.css";
import { Header, Grid, Input, Form, Button } from "semantic-ui-react";
import "./App.scss";
import questionsStore from "./store/QuestionsStore";
import Questions from "./models/Questions";
import QuestionCard from "./components/QuestionCard";

interface IProps {}

interface IState {
  qid: string;
}

@observer
class App extends Component<IProps, IState> {
  constructor(props: Readonly<IProps>) {
    super(props);
    this.state = {
      qid: ""
    };
    questionsStore.getInitialData();
  }

  render() {
    return (
      <div className="my-title">
        <Header className="my-header" size="huge">
          Corona Editor
        </Header>
        <Form
          onSubmit={() => {
            questionsStore.createNewCategory(this.state.qid);
            this.setState({ qid: "" });
          }}
        >
          <Form.Field>
            <div className="my-form">
              <Input
                placeholder="qid..."
                value={this.state.qid}
                onChange={(e: any) => {
                  this.setState({ qid: e.target.value });
                }}
              ></Input>
              <Button type="submit">Add New Category</Button>
            </div>
          </Form.Field>
        </Form>
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

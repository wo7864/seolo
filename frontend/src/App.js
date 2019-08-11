import React, { Component } from "react";
import "./App.css";
import TextItem from "./TextItem";
import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

class App extends Component {
  state = {
    sParam1 : "50",
    sParam2 : "40",
    sParam3 : "30",
    value: "",
    submit: "default",//제출된 텍스트를 담을 곳 , default 이미지가 존재해야함
    textList: []
  };

  componentDidMount() {
    this._renderText();
  }
  render() {
    const { textList } = this.state;
    console.log(textList);
    return (
      <div className="App">
      <input type="range" value={this.state.sParam1}  onChange={this._handleSliderChange1}/>
      <br/>
      <input type="range" value={this.state.sParam2}  onChange={this._handleSliderChange2}/>
      <br/>
      <input type="range" value={this.state.sParam3}  onChange={this._handleSliderChange3}/>
        <h1>OneLine App</h1>
        <div>
          <label>
            Text:
            <input
              type="text"
              value={this.state.value}
              onChange={this._handleTextChange}
            />
          </label>
          <button onClick={this._handleTextSubmit}>submit</button>
        </div>
        <h2>Long Text</h2>
        {textList.map((text, index) => {
          return (
            <TextItem
              text={text.text}
              key={index}
              id={text.id}
              handleClick={this._deleteText}
            />
          );
        })}
        <img src='https://www.valentinog.com/blog/wp-content/uploads/2018/03/django-rest-react@2x-1024x512.png' alt="이미지자리"/>
        <br/>
        {/*<img src={require('./images/'+this.state.submit+'.jpg')} alt="이미지자리"/>*/}
      </div>
    );
  }
  _handleSliderChange1 = event => {
    this.setState({ sParam1 : event.target.value });
  };
  _handleSliderChange2 = event => {
    this.setState({ sParam2 : event.target.value });
  };
  _handleSliderChange3 = event => {
    this.setState({ sParam3 : event.target.value });
  };
  _handleTextChange = event => {
    this.setState({ value : event.target.value });
  };
  _handleTextSubmit = () => {
    const { value } = this.state;
    const { sParam1 } = this.state;
    const { sParam2 } = this.state;
    const { sParam3 } = this.state;
    //텍스트 박스에 있는 내용을 value에 담고 그걸 this.state.submit에 넣어줌
    this.setState({ submit : value });
    this.setState({ sParam1 : sParam1 });
    this.setState({ sParam2 : sParam2 });
    this.setState({ sParam3 : sParam3 });
    axios
    //calligraphy
      .post("http://localhost:8000/api/wisesaying/", { text: value+"_"+sParam1+"_"+sParam2+"_"+sParam3 })
      .then(res => this._renderText());
  };
  _renderText = () => {
    axios
      .get("http://localhost:8000/api/wisesaying/")
      .then(res => this.setState({ textList: res.data }))
      .catch(err => console.log(err));
  };
  _deleteText = id => {
    axios.delete(`http://localhost:8000/api/wisesaying/${id}`).then(res => this._renderText());
  };
}

export default App;

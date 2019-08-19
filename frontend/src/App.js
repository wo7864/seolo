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
    sParam4 : "20",
    sParam5 : "10",
    value: "", // 사용자가 입력한 텍스트
    submit: "default",//제출된 텍스트를 담을 곳 , default 이미지가 존재해야함
    names : [],
    textList: []
  };
  
  componentDidMount() {
    this._renderText();
  }
  render() {
    const bg=require('./images/back2.png')
    const bgStyle ={
      backgroundImage: "url("+bg+")",
      position: 'absolute',
      top:'0', 
      left: '0',
      width: '100%',
      height: '100%',
    }
    const styleTitle = {
      fontSize : '80px',
      fontWeight : 'bold',
    }
    const styleSubTitle = {
      fontSize : '20px',
      fontWeight : 'bold',
    }
    const styleSubmit ={
      border : '0',
      borderRadius : '10px',
      backgroundColor : '#555555',
      width:'200px',
      color:'white',
      height:'25px',
    }
    const logoSize ={
      width: '350px',
      height: '225px',
      marginTop:'-60px',
      marginBottom:'-40px',
    }
    const inputStyle ={
      width: '200px',
      borderRadius:'10px',
      height:'20px',
    }
    const { textList } = this.state;
    //step 3.src 부분에 {name} 나중에 넣어주면 됨 왜냐하면 name 값에 url이 들어갈 거기 때문 현재는 고정 src로 테스트
    const nameList = this.state.names.map( (name,index) => (<img key={index} src={name} alt="이미지 찾지 못함"/>));
    return (
      <div className="App"  style ={ bgStyle}>
      <br/>
      <br/>
      <br/>
      <p style={styleSubTitle}>예쁜 손글씨를 빠르게 만들어보세요!</p>
        <img src={require('./images/logo.png')} style={logoSize}/>
        <div>
          <p>
            <input
              type="text"
              value={this.state.value}
              onChange={this._handleTextChange}
              style={inputStyle}
            />
          </p>
          <button style={styleSubmit} onClick={this._handleTextSubmit}>제출</button>
          <br/><br/>
          Bold - low <input type="range" value={this.state.sParam1}  onChange={this._handleSliderChange1}/>
          <br/>
          Bold - high <input type="range" value={this.state.sParam2}  onChange={this._handleSliderChange2}/>
          <br/>
          Italic - low <input type="range" value={this.state.sParam3}  onChange={this._handleSliderChange3}/>
          <br/>
          Italic - high <input type="range" value={this.state.sParam4}  onChange={this._handleSliderChange4}/>
          <br/>
          Kerning &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="range" value={this.state.sParam5}  onChange={this._handleSliderChange5}/>
          <br/>
        </div>
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
        <br/>
       {nameList}
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
  _handleSliderChange4 = event => {
    this.setState({ sParam4 : event.target.value });
  };
  _handleSliderChange5 = event => {
    this.setState({ sParam5 : event.target.value });
  };
  _handleTextChange = event => {
    this.setState({ value : event.target.value });
    this.setState({  name : event.target.value /*step 1.여기에 생성된 이미지의 url을 주면 됨*/ });
  };
  _handleTextSubmit = () => {
    const { value } = this.state;
    const { sParam1 } = this.state;
    const { sParam2 } = this.state;
    const { sParam3 } = this.state;
    const { sParam4 } = this.state;
    const { sParam5 } = this.state;
    //텍스트 박스에 있는 내용을 value에 담고 그걸 this.state.submit에 넣어줌
    this.setState({ submit : value });
    this.setState({ sParam1 : sParam1 });
    this.setState({ sParam2 : sParam2 });
    this.setState({ sParam3 : sParam3 });
    this.setState({ sParam4 : sParam4 });
    this.setState({ sParam5 : sParam5 });

    axios
    //calligraphy로 api명 변경 필요
      .post("http://15.164.49.159:8000/api/callis", {name : value, param1 : sParam1, param2 : sParam2, param3 : sParam3, param4 : sParam4, param5 : sParam5,})
      .then(res =>{ 
        this._renderText();
        this.setState({
          //names : this.state.names.concat("url/"+value+"_"+sParam1+"_"+sParam2+"_"+sParam3+"_"+sParam4+"_"+sParam5+".png"),/*step 2.submit된 name 값을 맵에 넣어주고 name값 초기화*/
          // eslint-disable-next-line
          names : this.state.names.concat("https://calligrapick.s3.ap-northeast-2.amazonaws.com/result/"+value+"_"+sParam1+"_"+sParam2+"_"+sParam3+"_"+sParam4+"_"+sParam5+".png"),/*step 2.submit된 name 값을 맵에 넣어주고 name값 초기화*/
          name:'',
        });
        
      });
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

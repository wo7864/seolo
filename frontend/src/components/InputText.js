import React from 'react';
import '../css/InputText.css';


export default class InputText extends React.Component {
    constructor(props){
        super(props);
    }

    render(){
        return(
            <header className="masthead d-flex">
                <div className="container text-center my-auto">
                <h1 className="mb-1">서로</h1>
                <h3 className="mb-5">
                    인공지능 캘리그라퍼
                </h3>
                <div className="btn-list">
                    <button onClick={this.props.handleChange} name="font" value="0" className={"btn btn-primary font-btn font1 " + (this.props.font==0 ? 'isSelected' : '')}>동글</button>
                    <button onClick={this.props.handleChange} name="font" value="1" className={"btn btn-primary font-btn font1 " + (this.props.font==1 ? 'isSelected' : '')}>투박</button>
                    <button onClick={this.props.handleChange} name="font" value="2" className={"btn btn-primary font-btn font1 " + (this.props.font==2 ? 'isSelected' : '')}>얇은</button>
                </div>
                <input
                    placeholder="한글을 입력해주세요."
                    name="input_text"
                    value={this.props.input_text}
                    onChange={this.props.handleChange}
                    className="input-textbox"
                    />
                <a className="btn btn-primary btn-xl js-scroll-trigger font1 create-btn"
                onClick={this.props.create_image}  href="#about">Let's Create!</a>
                </div>
                <div className="overlay"></div>
            </header>
        )
    }
}


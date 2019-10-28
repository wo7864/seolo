import React from 'react';


export default class ShowImage extends React.Component {
    constructor(props){
        super(props);

    }
    render(){
        let filename = this.props.filename

        const img_dir = 'file:///C:/Users/wo786/api/static/image/'+filename;
        const image = (
            <a href={img_dir}>
                <img src={img_dir}/>
            </a>
        )
        return(
            <div>
                <h1>서로 - 서예 로봇</h1>
                <span>폰트종류: </span>
                <select onChange={this.props.fontChange}>
                    <option value="0">날린 글씨</option>
                    <option value="1">구수한 글씨</option>
                    <option value="2">동그란 글씨</option>
                </select>
                <br/>
                <input
                    placeholder="한글을 입력해주세요."
                    name="input_text"
                    value={this.props.input_text}
                    onChange={this.props.handleChange}
                    />
                <button onClick={this.props.create_image}>생성</button>
                <br/>
            </div>
        )
    }
}


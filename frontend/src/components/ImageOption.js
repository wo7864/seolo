import React from 'react';

export default class PhonemeList extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            isHide:true
        }
        this.setHide = this.setHide.bind(this);
    }

    setHide(){
        let isHide = !this.state.isHide;
        this.setState({
            isHide: isHide
        })
    }

    render(){
        let html = '';
        if(this.state.isHide === true){
            html = 
            <div>
                <button onClick={this.setHide}>용지 옵션 보기</button>
            </div>
        }
        else{
            html = 
            <div>
                <button onClick={this.setHide}>
                    숨기기
                </button>
                <br/>
                <span>선명도</span>
                <input value={this.props.definition} type="range"
                    onChange={this.props.handleChange}
                    name="definition"/>
                <p>전체 용지 크기</p>
                <span>가로</span>
                <input value={this.props.image_width}  
                    onChange={this.props.handleChange}
                    name="image_width"/>
                <span>세로</span>
                <input value={this.props.image_height} 
                    onChange={this.props.handleChange}
                    name="image_height"/>
                <br/>
                <span>R</span>
                <input value={this.props.color[0]} 
                    onChange={this.props.set_color}
                    name="red"/>
                <span>G</span>
                <input value={this.props.color[1]} 
                    onChange={this.props.set_color}
                    name="green"/>
                <span>B</span>
                <input value={this.props.color[2]} 
                    onChange={this.props.set_color}
                    name="blue"/>
                <br/>
                <button onClick={this.props.set_image_option}>
                    적용
                </button>
            </div>
        }           
        return(
            <div>
                {html}
            </div>
        )
    }
}

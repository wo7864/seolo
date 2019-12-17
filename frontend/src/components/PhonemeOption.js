import React from 'react';
import '../css/PhonemeOption.css';

export default class PhonemeOption extends React.Component {
    constructor(props){
        super(props);
        this.state={
            selected:-1
        }
        this.close_dic = this.close_dic.bind(this);
    }

    open_dic(num){
        this.setState({
            selected:num
        })
    }

    select_img(i, j){
        this.props.update_phoneme_shape(this.state.selected, (i-2)/2, (j-2)/2);
        this.close_dic();
    }

    close_dic(){
        this.setState({
            selected:-1
        })
    }
    

    render(){
        
        const before_select = (
            <div>
                <h3>{this.props.phoneme2}</h3>
                <p>
                    <button class="shape-btn" onClick={() => this.open_dic(0)}>
                        <img src={this.props.img_dic[0][2][2]} className="shape-img" alt=""/>
                    </button>
                    <button class="shape_btn" onClick={() => this.open_dic(1)}>
                        <img src={this.props.img_dic[1][2][2]} className="shape-img" alt=""/>
                    </button>
                    <button class="shape_btn" onClick={() => this.open_dic(2)}>
                        <img src={this.props.img_dic[2][2][2]} className="shape-img" alt=""/>
                    </button>
                    <button class="shape_btn" onClick={() => this.open_dic(3)}>
                        <img src={this.props.img_dic[3][2][2]} className="shape-img" alt=""/>
                    </button>
                    <button class="shape_btn" onClick={() => this.open_dic(4)}>
                        <img src={this.props.img_dic[4][2][2]} className="shape-img" alt=""/>
                    </button>
                </p>
                <div class="inline-block text-center width-50">
                    <div class="inline-block text-center">
                        <span>X </span><br/>
                        <input name="x" className="custom_textbox"
                            value={this.props.latter_list[this.props.latter][this.props.phoneme].x} 
                            onChange={this.props.change_value} onBlur={this.props.update_phoneme_location}/>&nbsp;
                    </div>
                    <div class="inline-block text-center">
                        <span>Y </span><br/>
                        <input name="y" className="custom_textbox"
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].y} 
                        onChange={this.props.change_value} onBlur={this.props.update_phoneme_location}/>
                    </div>
                </div>
                
                <div class="inline-block text-center width-50">
                    <span>Rotation</span><br/>
                    <input type="range" name="rotation" className="range-custom small-range" min="-90" max="90" step="1"
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].rotation} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_rotation}/><br/>
                </div>
                <br/>
                <div class="inline-block text-center width-50">
                <span>Width</span><br/>
                <input type="range" name="width" className="range-custom small-range" min="40" max="150"
                    value={this.props.latter_list[this.props.latter][this.props.phoneme].width} 
                    onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_size}/><br/>
                </div>
                <div class="inline-block text-center width-50">
                <span>Height </span><br/>
                <input type="range" name="height" className="range-custom small-range" min="40" max="150"
                    value={this.props.latter_list[this.props.latter][this.props.phoneme].height} 
                    onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_size}/><br/>
                </div>
                {!this.props.real_time && <button onClick={this.props.update_phoneme} className="save-btn">적용</button>}
            </div>)

        let after_select = [];
        if(this.state.selected>=0){
            for(let i=0; i<5;i++){
                for(let j=0; j<5; j++){
                    after_select.push(
                        <button class="shape-btn" onClick={() => this.select_img(i, j)}>
                            <img src={this.props.img_dic[this.state.selected][i][j]} className="shape-img" alt=""/>
                        </button>
                    )
                }
                after_select.push(<br/>);
            }
        }
        after_select.push(<button onClick={this.close_dic} className="back-btn"><img className="back-img" src="/images/back.svg"/></button>)
        return(
            
            <div className="text-center my-auto" >
                <div className="div_style">
                    {this.state.selected < 0 && before_select}
                    {this.state.selected >= 0 && after_select}
                </div>
            </div>
        )
    }
}

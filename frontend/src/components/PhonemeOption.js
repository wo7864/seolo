import React from 'react';

export default class PhonemeOption extends React.Component {
    constructor(props){
        super(props);
    }
    render(){
        const phoneme_list = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅑ', 'ㅔ', 'ㅐ', 'ㅓ', 'ㅕ', 'ㅣ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', ' ', '\n']
        const div_style={
            display:"inline-block",
            marginLeft:"20px",
            width:"300px"
        }
        const div_style2={
            display:"inline-block",
            border:"1px solid black",
            borderRadius:"5px",
            padding:"10px",
            backgroundColor:"white",
        }
        const custom_textbox={
            width:"50px",
            height:"30px",
            border:"1px solid #aaa",
            borderRadius:"5px",
            marginBottom:"3px",
            padding:"5px"
        }
        let params = this.props.latter_list[this.props.latter][this.props.phoneme].params;
        let sample = [];
        let phoneme_num = 0;
        let tmp = 0;
        let filename = '';
        for(let i=0;i<4;i++){
            for(let j=0;j<101;j+=100){
                phoneme_num = phoneme_list.indexOf(this.props.phoneme2);
                tmp = params[i];
                params[i] = j;
                filename = this.props.font + "_" + phoneme_num + "_" + params[0] + "_" + params[1] + "_" + params[2] + "_" + params[3] + ".png";
                sample.push(filename);
                params[i] = tmp;
            }
        }
        console.log(sample);

        return(
            <div class="text-center my-auto" >
                <div style={div_style2}>
                <div style={div_style}>
                    <h3>{this.props.phoneme2}</h3>
                    <p>
                    <img src={sample[0]}/>
                    <input type="range" name="p1" class="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[0]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={sample[1]}/>
                    </p>
                    <p>
                    <img src={sample[2]}/>
                    <input type="range" name="p2" class="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[1]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={sample[3]}/>
                    </p>
                    <p>
                    <img src={sample[4]}/>
                    <input type="range" name="p3" class="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[2]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={sample[5]}/>
                    </p>
                    <p>
                    <img src={sample[6]}/>
                    <input type="range" name="p4" class="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[3]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={sample[7]}/>
                    </p>
                </div>
                <div style={div_style}>
                    <span>X </span>
                    <input name="x" style={custom_textbox}
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].x} 
                        onChange={this.props.change_value} onBlur={this.props.update_phoneme_location}/>&nbsp;
                    <span>Y </span>
                    <input name="y" style={custom_textbox}
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].y} 
                        onChange={this.props.change_value} onBlur={this.props.update_phoneme_location}/><br/>
                    <span>rotation</span><br/>
                    <input type="range" name="rotation" class="custom-range" min="-90" max="90" step="1"
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].rotation} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_rotation}/><br/>
                    <span>width</span><br/>
                    <input type="range" name="width" class="custom-range" min="40" max="150"
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].width} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_size}/><br/>
                    <span>height </span><br/>
                    <input type="range" name="height" class="custom-range" min="40" max="150"
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].height} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_size}/><br/>
                </div><br/>
                    {this.props.real_time && <button onClick={this.props.toggle_real_time} class="btn btn-primary">실시간 변환</button>}
                    {!this.props.real_time && <button onClick={this.props.toggle_real_time} class="btn btn-primary">일괄 변환</button>}
                    {!this.props.real_time && <button onClick={this.props.update_phoneme} class="btn btn-primary">적용</button>}
                </div>

            </div>
        )
    }
}

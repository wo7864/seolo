import React from 'react';
import '../css/PhonemeOption.css';

export default class PhonemeOption extends React.Component {
    constructor(props){
        super(props);
    }
    render(){


        return(
            <div class="text-center my-auto" >
                <div class="div_style2">
                <div class="div_style">
                    <h3>{this.props.phoneme2}</h3>
                    <p>
                    <img src={this.props.sample[0]} class="sample_img"/>
                    <input type="range" name="p1" class="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[0]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={this.props.sample[1]} class="sample_img"/>
                    </p>
                    <p>
                    <img src={this.props.sample[2]} class="sample_img"/>
                    <input type="range" name="p2" class="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[1]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={this.props.sample[3]} class="sample_img"/>
                    </p>
                    <p>
                    <img src={this.props.sample[4]} class="sample_img"/>
                    <input type="range" name="p3" class="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[2]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={this.props.sample[5]} class="sample_img"/>
                    </p>
                    <p>
                    <img src={this.props.sample[6]} class="sample_img"/>
                    <input type="range" name="p4" class="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[3]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={this.props.sample[7]} class="sample_img"/>
                    </p>
                </div>
                <div class="div_style">
                    <span>X </span>
                    <input name="x" class="custom_textbox"
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].x} 
                        onChange={this.props.change_value} onBlur={this.props.update_phoneme_location}/>&nbsp;
                    <span>Y </span>
                    <input name="y" class="custom_textbox"
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
                    {this.props.real_time && <button onClick={this.props.toggle_real_time} class="btn btn-primary">실시간 변환</button>}
                    {!this.props.real_time && <button onClick={this.props.toggle_real_time} class="btn btn-primary">일괄 변환</button>}
                    {!this.props.real_time && <button onClick={this.props.update_phoneme} class="btn btn-primary">적용</button>}
                </div><br/>
                    
                </div>

            </div>
        )
    }
}

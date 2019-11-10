import React from 'react';
import '../css/PhonemeOption.css';

export default class PhonemeOption extends React.Component {

    render(){
        return(
            <div className="text-center my-auto" >
                <div className="div_style">
                    <h3>{this.props.phoneme2}</h3>
                    <p>
                    <img src={this.props.sample[0]} className="sample_img" alt=""/>
                    <input type="range" name="p1" className="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[0]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={this.props.sample[1]} className="sample_img" alt=""/>
                    </p>
                    <p>
                    <img src={this.props.sample[2]} className="sample_img" alt=""/>
                    <input type="range" name="p2" className="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[1]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={this.props.sample[3]} className="sample_img" alt=""/>
                    </p>
                    <p>
                    <img src={this.props.sample[4]} className="sample_img" alt=""/>
                    <input type="range" name="p3" className="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[2]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={this.props.sample[5]} className="sample_img" alt=""/>
                    </p>
                    <p>
                    <img src={this.props.sample[6]} className="sample_img" alt=""/>
                    <input type="range" name="p4" className="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[3]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={this.props.sample[7]} className="sample_img" alt=""/>
                    </p>
                    <span>X </span>
                    <input name="x" className="custom_textbox"
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].x} 
                        onChange={this.props.change_value} onBlur={this.props.update_phoneme_location}/>&nbsp;
                    <span>Y </span>
                    <input name="y" className="custom_textbox"
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].y} 
                        onChange={this.props.change_value} onBlur={this.props.update_phoneme_location}/>
                    <span>rotation</span>
                    <input type="range" name="rotation" className="custom-range small-range" min="-90" max="90" step="1"
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].rotation} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_rotation}/><br/>
                    <span>width</span>
                    <input type="range" name="width" className="custom-range small-range" min="40" max="150"
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].width} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_size}/><br/>
                    <span>height </span>
                    <input type="range" name="height" className="custom-range small-range" min="40" max="150"
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].height} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_size}/><br/>
                    {this.props.real_time && <button onClick={this.props.toggle_real_time} className="btn btn-primary">실시간 변환</button>}
                    {!this.props.real_time && <button onClick={this.props.toggle_real_time} className="btn btn-primary">일괄 변환</button>}&nbsp;&nbsp;
                    {!this.props.real_time && <button onClick={this.props.update_phoneme} className="btn btn-primary">적용</button>}
                </div>
            </div>
        )
    }
}

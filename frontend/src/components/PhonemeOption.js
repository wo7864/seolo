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
                    <input type="range" name="p1" className="range-custom medium-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[0]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={this.props.sample[1]} className="sample_img" alt=""/>
                    </p>
                    <p>
                    <img src={this.props.sample[2]} className="sample_img" alt=""/>
                    <input type="range" name="p2" className="range-custom medium-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[1]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={this.props.sample[3]} className="sample_img" alt=""/>
                    </p>
                    <p>
                    <img src={this.props.sample[4]} className="sample_img" alt=""/>
                    <input type="range" name="p3" className="range-custom medium-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[2]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={this.props.sample[5]} className="sample_img" alt=""/>
                    </p>
                    <p>
                    <img src={this.props.sample[6]} className="sample_img" alt=""/>
                    <input type="range" name="p4" className="range-custom medium-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[3]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/>
                    <img src={this.props.sample[7]} className="sample_img" alt=""/>
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
                </div>
            </div>
        )
    }
}

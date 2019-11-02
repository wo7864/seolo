import React from 'react';

export default class PhonemeOption extends React.Component {
    constructor(props){
        super(props);
    }
    render(){
        const div_style={
            display:"inline-block",
            marginLeft:"20px"
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

        return(
            <div class="text-center my-auto" >
                <div style={div_style2}>
                <div style={div_style}>
                    <h3>{this.props.phoneme2}</h3>
                    <span>p1</span>
                    <input type="range" name="p1" class="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[0]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/><br/>
                    <span>p2</span>
                    <input type="range" name="p2" class="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[1]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/><br/>
                    <span>p3</span>
                    <input type="range" name="p3" class="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[2]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/><br/>
                    <span>p4</span>
                    <input type="range" name="p4" class="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].params[3]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_shape}/><br/>
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
                    <input type="range" name="width" class="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].width} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_size}/><br/>
                    <span>height </span><br/>
                    <input type="range" name="height" class="custom-range" 
                        value={this.props.latter_list[this.props.latter][this.props.phoneme].height} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_phoneme_size}/><br/>
                </div>
                </div>
            </div>
        )
    }
}

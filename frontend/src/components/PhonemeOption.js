import React from 'react';

export default class Option extends React.Component {
    render(){
        const div_style={
            float:"left",
            marginLeft:"20px"
        }
        const btn_style={
            width:"40px",
            height:"40px"
        }
        const move_div={
            marginLeft:"60px"
        }
        const ten_space = <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        return(
            <div>
                <div style={div_style}>
                    <h3>{this.props.phoneme}</h3>
                    <span>p1</span>
                    <input type="range" name="p1" value={this.props.latter_list[this.props.latter][this.props.phoneme].params[0]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_image}/><br/>
                    <span>p2</span>
                    <input type="range" name="p2" value={this.props.latter_list[this.props.latter][this.props.phoneme].params[1]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_image}/><br/>
                    <span>p3</span>
                    <input type="range" name="p3" value={this.props.latter_list[this.props.latter][this.props.phoneme].params[2]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_image}/><br/>
                    <span>p4</span>
                    <input type="range" name="p4" value={this.props.latter_list[this.props.latter][this.props.phoneme].params[3]} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_image}/><br/>
                </div>
                <div style={div_style}>
                    <span>x</span>
                    <input name="x" value={this.props.latter_list[this.props.latter][this.props.phoneme].x} 
                        onChange={this.props.change_value}/><br/>
                    <span>y</span>
                    <input name="y" value={this.props.latter_list[this.props.latter][this.props.phoneme].y} 
                        onChange={this.props.change_value}/><br/>
                    <br/>
                    <span>width &nbsp;&nbsp;</span>
                    <input type="range" name="width" value={this.props.latter_list[this.props.latter][this.props.phoneme].width} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_image}/><br/>
                    <span>height </span>
                    <input type="range" name="height" value={this.props.latter_list[this.props.latter][this.props.phoneme].height} 
                        onChange={this.props.change_value} onMouseUp={this.props.update_image}/><br/>
                </div>
            </div>
        )
    }
}

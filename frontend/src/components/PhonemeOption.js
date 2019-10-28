import React from 'react';
import axios from 'axios';
const domain = "http://127.0.0.1:5000/calligraphy";

export default class Option extends React.Component {
    constructor(props){
        super(props);
    }


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
                    <div style={move_div}>
                        {ten_space}
                        <button name="up" onClick={this.props.change_value} style={btn_style}>↑</button><br/>
                        <button name="left" onClick={this.props.change_value} style={btn_style}>←</button>
                        {ten_space}&nbsp;
                        <button name="right" onClick={this.props.change_value} style={btn_style}>→</button><br/>
                        {ten_space}
                        <button name="down" onClick={this.props.change_value} style={btn_style}>↓</button>
                    </div>
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

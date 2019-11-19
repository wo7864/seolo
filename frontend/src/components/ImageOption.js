import React from 'react';
import '../css/ImageOption.css';

export default class PhonemeList extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            cs_active:false
        }
        this.active_cs = this.active_cs.bind(this);

    }
    active_cs(){
        if(!this.props.is_invisiable){
            alert("투명성을 체크해야 해당 속성을 이용할 수 있습니다.");
            return;
        }
        let target = !this.state.cs_active;
        this.setState({
            cs_active:target
        })
    }
    deactive_cs(i){
        this.props.set_color(i);
        this.setState({
            cs_active:false
        })
    }
    render(){

        let color_style = "";
        if(this.state.color !== ""){
            color_style = {
                backgroundColor:"#"+this.props.color
            }
        }

        const color_list = ['000000', '444444', '888888', 'bbbbbb', 'ffffff', 
                            '79a38f', 'c1d099', 'f5eaaa', 'f5be8f', 'e1837b', 
                            '9bbaab', 'd1dcb2', 'f9eec0', 'f7cda9', 'e8a19b', 
                            'bdd1c8', 'e1e7cd', 'faf4d4', 'fbdfc9', 'f1c1bd'];
        let color_li_list = [];
        let color_option_list = [];
        for(let i of color_list){
            color_li_list.push(<li class={"color-" + i} data-option="" data-value={"#" + i} onClick={this.deactive_cs.bind(this, i)}><span>{"#" + i}</span></li>);
            color_option_list.push(<option value={"#" + i} data-class={"color-" + i} >{"#" + i}</option>);
        }


        let html =
            <div class="text-center my-auto">
                <div class="inline-block width-100">
                    <div class={"cs-select cs-skin-boxes fs-anim-lower " + (this.state.cs_active ? "cs-active" : "")} tabindex="0">
                        <span class="cs-placeholder" onClick={this.active_cs} style={color_style}>{this.props.color ? "#" + this.props.color : "Pick a color"}</span>
                        <div class="cs-options">
                            <ul>
                                {color_li_list}
                            </ul>
                        </div>
                        <select class="cs-select cs-skin-boxes fs-anim-lower" name="color" onChange={this.handleChange}>
                            <option value="" disabled="" selected="">Pick a color</option>
                            {color_option_list}
                        </select>
                    </div>
                    <div class="inline-block">
                        <span>흐림</span>
                        <input value={this.props.blur} 
                            type="range"
                            className="range-custom"
                            onChange={this.props.handleChange}
                            name="blur"
                            min="0"
                            max="5"
                            step="1"
                            onMouseUp={this.props.update_image_option}/><br/>
                        <input type="checkbox"
                            checked={this.props.is_invisiable}  
                            onChange={this.props.checkboxChange}
                            name="is_invisiable"/>
                        <span>투명성</span>

                    </div>
                </div>                
            </div>
        return(
            <div>
                {html}
            </div>
        )
    }
}

import React from 'react';
import '../css/ImageOption.css';

export default class PhonemeList extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            isHide:false
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
        let html =
            <div>
            <a class="menu-toggle rounded" onClick={this.setHide}>
                <i class={"fas " + (this.state.isHide ? "fa-times" : "fa-bars")}></i>
            </a>

            <nav id="sidebar-wrapper" class={(this.state.isHide ? "active" : "")}>
                <ul class="sidebar-nav">
                    <li class="sidebar-brand normal-font white">
                        이미지 옵션
                    </li>
                    <li class="sidebar-nav-item">
                        <span>blur</span>
                        <input value={this.props.blur} 
                            type="range"
                            class="custom-range"
                            onChange={this.props.handleChange}
                            name="blur"
                            min="0"
                            max="5"
                            step="1"/>
                    </li>
                    <li class="sidebar-nav-item">
                        <span>R</span>
                        <input value={this.props.color[0]} 
                            type="range"
                            class="custom-range"
                            onChange={this.props.set_color}
                            name="red"
                            max="255"/>
                    </li>
                    <li class="sidebar-nav-item">
                        <span>G</span>
                        <input value={this.props.color[1]}
                            type="range"
                            class="custom-range" 
                            onChange={this.props.set_color}
                            max="255"
                            name="green"/>
                    </li>
                    <li class="sidebar-nav-item">
                        <span>B</span>
                        <input value={this.props.color[2]} 
                            type="range"
                            class="custom-range" 
                            onChange={this.props.set_color}
                            max="255"
                            name="blue"/>
                    </li>
                    <li class="sidebar-nav-item">
                        <span>가로</span>
                        <input value={this.props.image_width}
                            class="side-input-text"  
                            onChange={this.props.handleChange}
                            name="image_width"/>
                    </li>
                    <li class="sidebar-nav-item">
                        <span>세로</span>
                        <input value={this.props.image_height} 
                            class="side-input-text"  
                                onChange={this.props.handleChange}
                                name="image_height"/>
                    </li>
                    <li class="sidebar-nav-item">
                        <input type="checkbox"
                            checked={this.props.is_invisiable}  
                            onChange={this.props.checkboxChange}
                            name="is_invisiable"/>
                        <span>투명성</span>

                    </li>
                    
                        <button 
                            onClick={this.props.update_image_option}
                            class="save-btn rounded normal-font">
                            적용
                        </button>   
                        <li>
                            <br/>
                        </li>
                        <li class="sidebar-brand normal-font white">
                            배경 옵션
                        </li>
                        {!this.props.cb_filename &&
                        <li class="sidebar-nav-item">
                            <label htmlFor="file-input"
                            class="file-label normal-font">배경 업로드</label>
                            <input type="file" 
                                id="file-input"
                                name="bg_image"
                                class="file-input"
                                onChange={this.props.handleImage}/>
                        </li>
                        }
                        {this.props.cb_filename &&
                        <li class="sidebar-nav-item">
                            <span class="normal-font white">X</span>
                            <input value={this.props.x_in_bg} 
                                class="side-input-text custom_textbox"  
                                    onChange={this.props.handleChange}
                                    name="x_in_bg"/>&nbsp;&nbsp;&nbsp;
                            <span class="normal-font white">Y</span>
                            <input value={this.props.y_in_bg} 
                                class="side-input-text custom_textbox"  
                                onChange={this.props.handleChange}
                                name="y_in_bg"/>
                        </li>
                        }
                        {this.props.cb_filename &&
                        <li class="sidebar-nav-item">
                            <button class="delete-btn rounded normal-font">
                                배경 제거</button>
                        </li>
                        }

                    </ul>     
                </nav>
            </div>
        return(
            <div>
                {html}
            </div>
        )
    }
}

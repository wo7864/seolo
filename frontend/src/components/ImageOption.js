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
            <li className="sidebar-nav-item">
                <span>blur</span>
                <input value={this.props.blur} 
                    type="range"
                    className="custom-range"
                    onChange={this.props.handleChange}
                    name="blur"
                    min="0"
                    max="5"
                    step="1"/>
            </li>
            <li className="sidebar-nav-item">
                <span>R</span>
                <input value={this.props.color[0]} 
                    type="range"
                    className="custom-range"
                    onChange={this.props.set_color}
                    name="red"
                    max="255"/>
            </li>
            <li className="sidebar-nav-item">
                <span>G</span>
                <input value={this.props.color[1]}
                    type="range"
                    className="custom-range" 
                    onChange={this.props.set_color}
                    max="255"
                    name="green"/>
            </li>
            <li className="sidebar-nav-item">
                <span>B</span>
                <input value={this.props.color[2]} 
                    type="range"
                    className="custom-range" 
                    onChange={this.props.set_color}
                    max="255"
                    name="blue"/>
            </li>
            <li className="sidebar-nav-item">
                <span>가로</span>
                <input value={this.props.image_width}
                    className="side-input-text"  
                    onChange={this.props.handleChange}
                    name="image_width"/>
            </li>
            <li className="sidebar-nav-item">
                <span>세로</span>
                <input value={this.props.image_height} 
                    className="side-input-text"  
                        onChange={this.props.handleChange}
                        name="image_height"/>
            </li>
            <li className="sidebar-nav-item">
                <input type="checkbox"
                    checked={this.props.is_invisiable}  
                    onChange={this.props.checkboxChange}
                    name="is_invisiable"/>
                <span>투명성</span>

            </li>
            
                <button 
                    onClick={this.props.update_image_option}
                    className="save-btn rounded normal-font">
                    적용
                </button>   
                <li>
                    <br/>
                </li>
                {!this.props.cb_filename &&
                <li className="sidebar-nav-item">
                    <label htmlFor="file-input"
                    className="file-label normal-font">배경 업로드</label>
                    <input type="file" 
                        id="file-input"
                        name="bg_image"
                        className="file-input"
                        onChange={this.props.handleImage}/>
                </li>
                }
                {this.props.cb_filename &&
                <div>
                    <li className="sidebar-nav-item">
                        <span className="normal-font white">X</span>
                        <input value={this.props.x_in_bg} 
                            className="side-input-text custom_textbox"  
                                onChange={this.props.handleChange}
                                name="x_in_bg"/>&nbsp;&nbsp;&nbsp;
                        <span className="normal-font white">Y</span>
                        <input value={this.props.y_in_bg} 
                            className="side-input-text custom_textbox"  
                            onChange={this.props.handleChange}
                            name="y_in_bg"/>
                    </li>

                    <li className="sidebar-nav-item">
                        <button className="delete-btn rounded normal-font"
                            onClick={this.props.set_location_in_bg}>
                            적용</button>
                        <button className="delete-btn rounded normal-font"
                            onClick={this.props.remove_background}>
                            배경 제거</button>
                    </li>
                </div>
                }
            </div>
        return(
            <div>
                {html}
            </div>
        )
    }
}

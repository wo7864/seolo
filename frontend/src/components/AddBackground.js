import React from 'react';
import '../css/AddBackground.css';


export default class AddBackground extends React.Component {
    constructor(props){
        super(props);
    }
    render(){
        const html = (
            <div>
                {!this.props.cb_filename &&
                <li className="sidebar-nav-item">
                    <label htmlFor="file-input"
                    className="file-label">+</label>
                    <input type="file" 
                        id="file-input"
                        name="bg_image"
                        className="file-input"
                        onChange={this.props.handleImage}/>
                </li>
                }
                {this.props.cb_filename &&
                <div>
                    <div class="inline-block text-center width-100">
                        <div class="inline-block text-center">
                            <span>X </span><br/>
                            <input value={this.props.x_in_bg} 
                                className="side-input-text custom_textbox"  
                                onChange={this.props.handleChange}
                                onBlur={this.props.set_location_in_bg}
                                name="x_in_bg"/>
                        </div>&nbsp;&nbsp;
                        <div class="inline-block text-center">
                            <span>Y </span><br/>
                            <input value={this.props.y_in_bg} 
                                className="side-input-text custom_textbox"  
                                onChange={this.props.handleChange}
                                onBlur={this.props.set_location_in_bg}
                                onBlur={this.props.set_location_in_bg}
                                name="y_in_bg"/>
                        </div><br/>
                        <button className="delete-btn rounded normal-font"
                        onClick={this.props.remove_background}>
                        X</button>
                    </div>

                </div>
                }
            </div>
        )

        return(
            <div>
                {html}

            </div>
        )
    }
}


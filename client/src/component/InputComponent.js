import React from 'react';
import '../style.css';


const fonts = ['font1', 'font2', 'font3'];
export default class InputComponent extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            selectedFont: 'font1',
        }
    }

    loadFonts = () => {
        return fonts.map((font, index) => {
            return (
                <div key={"font"+index}className="font-div">
                    <img className={this.state.selectedFont === font ? "font-image focus-font" : "font-image"}
                        src={'/images/'+font+'.png'}
                        onClick={() => this.setFont(font)} />
                    <button className="font-preview">미리보기</button>
                </div>
            )
        })
    }

    setFont(font) {
        this.setState({
            selectedFont: font
        })
    }
    handleChange() {

    }

    render() {
        return (
            <div className="container">

                <div className="left-container sub-container">
                    {this.loadFonts()}
                </div>
                <div className="right-container sub-container">
                    <input className="input-text" type="text"/>
                    <button className="submit-button">나만의 손글씨 만들기</button>
                </div>
            </div>
        )
    }
}
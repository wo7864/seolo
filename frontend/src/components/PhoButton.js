import React from 'react';


export default class PhoButton extends React.Component {
    render(){
        return(
            <button onClick={this.props.onClick} className={"pho-btn "+this.props.className}>
                {this.props.pho_name}
            </button>
        )
    }
}

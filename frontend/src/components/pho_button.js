import React from 'react';


export default class Option extends React.Component {
    render(){
        return(
            <button onClick={this.props.onClick} class={"pho-btn "+this.props.class}>
                {this.props.pho_name}
            </button>
        )
    }
}

import React from 'react';


export default class Option extends React.Component {
    render(){
        return(
            <button onClick={this.props.onClick}>
                {this.props.pho_name}
            </button>
        )
    }
}

import React from 'react';
import '../style.css';
export default class Header extends React.Component{

    constructor(props){
        super(props);

    }

    render(){
        return(
            <div className="header-div">
                서예로봇, 서로
            </div>
        )
    }
}
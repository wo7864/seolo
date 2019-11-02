import React from 'react';
import '../css/Header.css';


export default class ShowImage extends React.Component {
    render(){
        return(
            <nav class="navbar navbar-light bg-light static-top">
              <div class="container">
                <a class="navbar-brand" href="#">서로 - 서예 로봇</a>
                <a class="btn btn-primary" href="#">로그인</a>
              </div>
            </nav>
        )
    }
}


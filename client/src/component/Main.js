import React from 'react';
import Header from './Header';
import InputComponent from './InputComponent';
export default class Main extends React.Component {

    constructor(props) {
        super(props);

    }

    render() {
        return (
            <div>
                <Header />
                <InputComponent/>
            </div>
        )
    }
}
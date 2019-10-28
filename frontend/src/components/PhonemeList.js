import React from 'react';
import Pho_button from './pho_button';

export default class PhonemeList extends React.Component {
    constructor(props){
        super(props);
    }


    render(){
        let key = '';
        const data = this.props.latter_list.map((data2, i) =>{
            let list = data2.map((data3, j) =>{
                key = i + '_' + j;
                if(data3.phoneme !== ' '){
                    return (<Pho_button 
                        onClick={() => this.props.select_phoneme(i, j, data3.phoneme)} 
                        pho_name={data3.phoneme}
                        key={key}/>)
                }
            })
            list.push(<br key={i}/>)
            return list;
        })
        return(
            <div>
                {data}
            </div>
        )
    }
}

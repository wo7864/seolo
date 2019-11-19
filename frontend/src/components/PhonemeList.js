import React from 'react';
import PhoButton from './PhoButton';
import '../css/PhoButton.css';
export default class PhonemeList extends React.Component {
    render(){

        let key = '';
        const data = this.props.latter_list.map((data2, i) =>{
            let shape;
            let list = data2.map((data3, j) =>{
                key = i + '_' + j;
                if(data3.phoneme !== ' '){
                    shape = data3.shape_list;
                    return (<PhoButton 
                        onClick={() => this.props.select_phoneme(i, j, data3.phoneme)} 
                        pho_name={data3.phoneme}
                        className={"shape"+data3.shape_list.toString() +" latter"+ data3.latter_num.toString() +" phoneme"+ data3.phoneme_num.toString()}
                        key={key}/>)
                }
            })

            let list2 = <div class="latter_div" key={i}>{list}</div>
            return list2;
        })
        return(
            <div className="text-center my-auto">
                <div class="pho_list_div_style">
                    {data}
                </div>
            </div>
        )
    }
}

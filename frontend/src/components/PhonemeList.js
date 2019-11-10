import React from 'react';
import PhoButton from './PhoButton';
import '../css/PhoButton.css';
export default class PhonemeList extends React.Component {
    render(){
        const div_style = {
            display:"inline-block",
            padding:"10px",
            margin:"10px",
            border:"1px solid rgba(57,186,232,1)",
            borderRadius:"5px",
            backgroundColor:"rgba(57,186,232,0.2)"

        }

        const latter_div ={
            display:"inline-block",
            position:"relative",
            margin:"5px",
            padding:"2px",
            width:"80px",
            height:"80px",
            border:"0.5px solid #ccc",
            borderRadius:"3px",
            textAlign:"center",
            verticalAlign:"middle",
            backgroundColor:"white"

        }
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

            let list2 = <div style={latter_div} key={i}>{list}</div>
            return list2;
        })
        return(
            <div className="text-center my-auto">
                <div style={div_style}>
                    {data}
                </div>
            </div>
        )
    }
}

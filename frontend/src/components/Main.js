import React from 'react';
import PhonemeList from './PhonemeList';
import axios from 'axios';
import ShowImage from './ShowImage';
import Option from './Option';
import update from 'react-addons-update';

<<<<<<< HEAD
const domain = "http://52.78.51.15:5000/calligraphy";
=======
const domain = "http://127.0.0.1:5000/calligraphy";
>>>>>>> frontend

export default class Main extends React.Component {
    constructor(props){
        super(props);
        this.state={
<<<<<<< HEAD
            font:'type1',
=======
            font:0,
>>>>>>> frontend
            input_text:'',
            latter_list:[],
            select_phoneme:-1,
            filename:'',
            selected_latter:-1,
            selected_phoneme:-1,
            selected_phoneme2:''
        };
        this.create_image = this.create_image.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.fontChange = this.fontChange.bind(this);
        this.select_phoneme = this.select_phoneme.bind(this);
        this.update_image = this.update_image.bind(this);
        this.change_value = this.change_value.bind(this);
    }

    handleChange(e){
        this.setState({
            input_text: e.target.value
        });
    }
    fontChange(e){
        this.setState({
            font: e.target.value
        });
    }
    create_image(){
        axios.post(domain, 
            {
                input_text:this.state.input_text,
                font:this.state.font,
            })
            .then( response => { 
                this.setState({
                    filename:response.data.filename+".png",
                    latter_list:response.data.latter_list
                })
                console.log(response);
            })
            .catch( response => {console.log(response);});
        
    }

    select_phoneme(latter_num, phoneme_num, phoneme){
        this.setState({
            selected_latter:latter_num,
            selected_phoneme:phoneme_num,
            selected_phoneme2:phoneme
        })
    }

    change_value(e){
        let target = this.state.latter_list[this.state.selected_latter][this.state.selected_phoneme];
        if(e.target.name.slice(0,1) == 'p'){
            let idx = 0;
            if(e.target.name === 'p1') idx = 0;
            else if(e.target.name === 'p2') idx=1;
            else if(e.target.name === 'p3') idx=2;
            else if(e.target.name === 'p4') idx=3;
            target.params[idx] = e.target.value;
            this.setState({latter_list: update(this.state.latter_list, 
                {[this.state.selected_latter]:{[this.state.selected_phoneme]:{$set: target}}})})
        }
        else{
            if(e.target.name === 'width') {
                target.width = e.target.value;
                this.setState({latter_list: update(this.state.latter_list, 
                    {[this.state.selected_latter]:{[this.state.selected_phoneme]:{$set: target}}})})
            } else if(e.target.name === 'height'){
                target.height = e.target.value;
                this.setState({latter_list: update(this.state.latter_list, 
                    {[this.state.selected_latter]:{[this.state.selected_phoneme]:{$set: target}}})})
            }
            else{
                if(e.target.name === 'up') {
                    target.y--;
                    this.setState({latter_list: update(this.state.latter_list, 
                        {[this.state.selected_latter]:{[this.state.selected_phoneme]:{$set: target}}})})
                }
                else if(e.target.name === 'down') {
                    target.y++;
                    this.setState({latter_list: update(this.state.latter_list, 
                        {[this.state.selected_latter]:{[this.state.selected_phoneme]:{$set: target}}})})
                }
                else if(e.target.name === 'left') {
                    target.x--;
                    this.setState({latter_list: update(this.state.latter_list, 
                        {[this.state.selected_latter]:{[this.state.selected_phoneme]:{$set: target}}})})
                }
                else if(e.target.name === 'right') {
                    target.x++;
                    this.setState({latter_list: update(this.state.latter_list, 
                        {[this.state.selected_latter]:{[this.state.selected_phoneme]:{$set: target}}})})
                }
                this.update_image();
            }
        }
    }

    update_image(){
        let data = this.state.latter_list;
        let target = this.state.latter_list[this.state.selected_latter][this.state.selected_phoneme];
        data[this.state.selected_latter][this.state.selected_phoneme].params = 
            [target.params[0], target.params[1], target.params[2], target.params[3]];
        data[this.state.selected_latter][this.state.selected_phoneme].x = target.x;
        data[this.state.selected_latter][this.state.selected_phoneme].y = target.y;
        data[this.state.selected_latter][this.state.selected_phoneme].width = target.width;
        data[this.state.selected_latter][this.state.selected_phoneme].height = target.height;
        axios.put(domain, {
            latter_list:[data],
            latter_num: this.state.selected_latter,
            phoneme_num: this.state.selected_phoneme,
            input_text: this.state.input_text
        })
            .then( response => {
                this.setState({
                    filename:response.data.filename+".png",
                    latter_list:response.data.latter_list
                })
            })
            .catch( response => {console.log(response);});
    }

    render(){
        let korean_latter_list = [];
        let tmp = [];
        let latter_idx=0;
        let phoneme_idx=0;
        for(let i of this.state.latter_list){
            tmp = [];
            for(let j of i){
                tmp.push([j.phoneme, latter_idx, phoneme_idx]);
                phoneme_idx++;
            }
            latter_idx++;
            korean_latter_list.push(tmp);
        }
        return(
            <div>
                <h1>서로 - 서예 로봇</h1>
                <span>폰트종류: </span>
                <select onChange={this.fontChange}>
<<<<<<< HEAD
                    <option value="type1">동그란 글씨</option>
                    <option value="type2">날린 글씨</option>
                    <option value="type3">구수한 글씨</option>
=======
                    <option value="0">날린 글씨</option>
                    <option value="1">구수한 글씨</option>
                    <option value="2">동그란 글씨</option>
>>>>>>> frontend
                </select>
                <br/>
                <input
                    placeholder="한글을 입력해주세요."
                    name="input_text"
                    value={this.state.input_text}
                    onChange={this.handleChange}
                    />
                <button onClick={this.create_image}>생성</button>
                <br/>
                <PhonemeList 
                    update_image={this.update_image}
                    latter_list={this.state.latter_list}
                    input_text={this.state.input_text}
                    select_phoneme={this.select_phoneme}
                    latter={this.state.selected_latter}
                    phoneme={this.state.selected_phoneme}
                    phoneme2={this.state.selected_phoneme2}
                />
                {this.state.selected_phoneme != -1 && 
                <Option latter={this.state.selected_latter}
                    phoneme={this.state.selected_phoneme}
                    phoneme2={this.state.selected_phoneme2}
                    latter_list={this.state.latter_list}
                    update_image={this.update_image}
                    input_text={this.state.input_text}
                    change_value={this.change_value}
                    />
                }
                <br/>
                {this.state.filename !== '' ? <ShowImage filename={this.state.filename}/> : ''}
                
            </div>
        )
    }
}
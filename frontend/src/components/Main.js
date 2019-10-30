import React from 'react';
import PhonemeList from './PhonemeList';
import axios from 'axios';
import ShowImage from './ShowImage';
import PhonemeOption from './PhonemeOption';
import ImageOption from './ImageOption';
import update from 'react-addons-update';

//const domain ="http://127.0.0.1:5000/calligraphy";
import InputText from './InputText';
import SetBackGroundImage from './SetBackGroundImage';
const domain = "http://15.164.227.195:5000/calligraphy";

export default class Main extends React.Component {
    constructor(props){
        super(props);
        this.state={
            page:0,
            font:0,
            input_text:'',
            latter_list:[],
            select_phoneme:-1,
            filename:'',
            selected_latter:-1,
            selected_phoneme:-1,
            selected_phoneme2:'',
            definition:0,
            image_width:0,
            image_height:0,
            color:0,
            background_color:0
        };
        this.create_image = this.create_image.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.select_phoneme = this.select_phoneme.bind(this);
        this.update_image = this.update_image.bind(this);
        this.change_value = this.change_value.bind(this);
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
                    latter_list:response.data.latter_list,
                    page:1
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

    handleChange(e){
        let nextState = {};
        nextState[e.target.name] = e.target.value;
        this.setState(nextState);
    }

    set_image_option(){
        let data = this.state.latter_list;

        axios.put(domain+'image', {
            latter_list:[data],
            definition:this.state.definition,
            image_width:this.state.image_width,
            image_height:this.state.image_height,
            color:this.state.color,
            background_color:this.state.background_color
        })
            .then( response => {
                this.setState({
                    filename:response.data.filename+".png",
                    latter_list:response.data.latter_list
                })
            })
            .catch( response => {console.log(response);});
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
            font:this.state.font,
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
        let html = '';
        if(this.state.page == 0){
            html = 
            <InputText
                input_text={this.state.input_text}
                create_image={this.create_image}
                handleChange={this.handleChange}
                fontChange={this.fontChange}/>
        }else if(this.state.page == 1){
            html = 
            <div>
                <ImageOption
                    definition={this.state.definition}
                    image_width={this.state.image_width}
                    image_height={this.state.image_height}
                    handleChange={this.handleChange}
                    set_image_option={this.set_image_option}
                />
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
                <PhonemeOption 
                    phoneme={this.state.selected_phoneme2}
                    latter_list={this.state.latter_list}
                    update_image={this.update_image}
                    input_text={this.state.input_text}
                    handleChange={this.handleChange}
                    />
                }
                <br/>
                <ShowImage filename={this.state.filename}/>
            </div>
        }else if(this.state.page == 2){ // 이미지 배경합성하는 페이지
            html = 
            <div>
                <SetBackGroundImage/>
            </div>
        }

        return(
            <div>
                {html}
            </div>
        )
    }
}
import React from 'react';
import PhonemeList from './PhonemeList';
import axios from 'axios';
import ShowImage from './ShowImage';
import PhonemeOption from './PhonemeOption';
import ImageOption from './ImageOption';
import update from 'react-addons-update';
import InputText from './InputText';
import {Spinner} from 'react-bootstrap'
import '../css/Main.css';

const domain ="http://52.78.32.67:5000/calligraphy";

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
            blur:0,
            image_width:0,
            image_height:0,
            color:[1, 1, 1],
            is_invisiable:true,
            selected_file:null,
            bg_filename:'',
            cb_filename:'',
            is_loading:false,
            x_in_bg:0,
            y_in_bg:0,
            real_time:true,
            sample:[]
        };
        this.create_image = this.create_image.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.select_phoneme = this.select_phoneme.bind(this);
        this.change_value = this.change_value.bind(this);
        this.set_color = this.set_color.bind(this);
        this.update_image_option = this.update_image_option.bind(this);
        this.update_phoneme = this.update_phoneme.bind(this);
        this.update_phoneme_location = this.update_phoneme_location.bind(this);
        this.update_phoneme_shape = this.update_phoneme_shape.bind(this);
        this.update_phoneme_size = this.update_phoneme_size.bind(this);
        this.update_phoneme_rotation = this.update_phoneme_rotation.bind(this);
        this.update_background_image = this.update_background_image.bind(this);
        this.handleImage = this.handleImage.bind(this);
        this.checkboxChange = this.checkboxChange.bind(this);
        this.toggle_real_time = this.toggle_real_time.bind(this);
        this.get_sample = this.get_sample.bind(this);
    }

    create_image(){
        this.setState({
            is_loading:true
        })
        axios.post(domain, 
            {
                input_text:this.state.input_text,
                font:this.state.font,
            })
            .then( response => { 
                this.setState({
                    filename:response.data.filename,
                    latter_list:response.data.latter_list,
                    blur:response.data.blur,
                    color:response.data.color,
                    image_width:response.data.image_width,
                    image_height:response.data.image_height,
                    page:1,
                    is_loading:false
                })
                console.log(response);
            })
            .catch( response => {
                this.setState({
                    is_loading:false                    
                })
                console.log(response);
            });
    }
    get_sample(latter_num, phoneme_num, phoneme){
        axios.post(domain+'/sample', {
            latter_list:[this.state.latter_list],
            font:this.state.font,
            latter_num: latter_num,
            phoneme_num: phoneme_num,
        })
            .then( response => {
                const phoneme_list = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅑ', 'ㅔ', 'ㅐ', 'ㅓ', 'ㅕ', 'ㅣ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', ' ', '\n']

                let params = this.state.latter_list[latter_num][phoneme_num].params;
                let sample = [];
                let phoneme_num2 = 0;
                let tmp = 0;
                let filename = '';
                const s3_path = 'http://seolo.s3-website.ap-northeast-2.amazonaws.com/static/image/sample/';
                for(let i=0;i<4;i++){
                    for(let j=0;j<101;j+=100){
                        phoneme_num2 = phoneme_list.indexOf(phoneme);
                        tmp = params[i];
                        params[i] = j;
                        filename = this.state.font + "_" + phoneme_num2 + "_" + params[0] + "_" + params[1] + "_" + params[2] + "_" + params[3] + ".png";
                        sample.push(s3_path + filename);
                        params[i] = tmp;
                    }
                }
                this.setState({
                    is_loading:false,
                    sample:sample
                })
            })
            .catch( response => {
                this.setState({
                    is_loading:false                    
                })
                console.log(response);
            });
    }
    select_phoneme(latter_num, phoneme_num, phoneme){

        this.setState({
            is_loading:true,
            selected_latter:latter_num,
            selected_phoneme:phoneme_num,
            selected_phoneme2:phoneme
        })
        this.get_sample(latter_num, phoneme_num, phoneme);
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
            } else if(e.target.name === 'rotation'){
                target.rotation = e.target.value;
                this.setState({latter_list: update(this.state.latter_list, 
                    {[this.state.selected_latter]:{[this.state.selected_phoneme]:{$set: target}}})})
            }
            else{
                if(e.target.name === 'y') {
                    target.y = e.target.value*=1;
                    this.setState({latter_list: update(this.state.latter_list, 
                        {[this.state.selected_latter]:{[this.state.selected_phoneme]:{$set: target}}})})
                }else if(e.target.name === 'x') {
                    target.x = e.target.value*=1;
                    this.setState({latter_list: update(this.state.latter_list, 
                        {[this.state.selected_latter]:{[this.state.selected_phoneme]:{$set: target}}})})
                }
            }
        }
    }

    handleChange(e){
        let nextState = {};
        nextState[e.target.name] = e.target.value;
        this.setState(nextState);
    }
    checkboxChange(){
        let target = this.state.is_invisiable;
        this.setState({
            is_invisiable:!target
        })
    }

    update_image_option(){
        this.setState({
            is_loading:true
        })
        axios.put(domain+'/image', {
            latter_list:[this.state.latter_list],
            blur:this.state.blur,
            image_width:this.state.image_width,
            image_height:this.state.image_height,
            color:[this.state.color],
            is_invisiable:this.state.is_invisiable ? 1 : 0,
            input_text:this.state.input_text,
            bg_filename:this.state.bg_filename,
            x_in_bg:this.state.x_in_bg,
            y_in_bg:this.state.y_in_bg
        })
            .then( response => {
                this.setState({
                    filename:response.data.filename,
                    latter_list:response.data.latter_list,
                    is_loading:false
                })
            })
            .catch( response => {
                this.setState({
                    is_loading:false                    
                })
                console.log(response);
            });
    }


    toggle_real_time(){

        let target = !this.state.real_time;
        this.setState({
            real_time:target
        })
    }

   
    update_phoneme(){
        if(this.state.real_time)
            return;
        this.setState({
            is_loading:true
        })
        
        axios.put(domain, {
            latter_list:[this.state.latter_list],
            latter_num: this.state.selected_latter,
            phoneme_num: this.state.selected_phoneme,
            input_text: this.state.input_text,
            font:this.state.font,
            blur:this.state.blur,
            image_width:this.state.image_width,
            image_height:this.state.image_height,
            is_invisiable:this.state.is_invisiable ? 1 : 0,
            color:[this.state.color],
            bg_filename:this.state.bg_filename,
            x_in_bg:this.state.x_in_bg,
            y_in_bg:this.state.y_in_bg
        })
            .then( response => {
                this.setState({
                    filename:response.data.filename,
                    cb_filename:response.data.cb_filename,
                    latter_list:response.data.latter_list,
                    is_loading:false
                })
            })
            .catch( response => {
                this.setState({
                    is_loading:false                    
                })
                console.log(response);
            });    
    }

    update_phoneme_shape(){
        if(!this.state.real_time)
            return;
        this.setState({
            is_loading:true
        })
        
        axios.put(domain+'/shape', {
            latter_list:[this.state.latter_list],
            latter_num: this.state.selected_latter,
            phoneme_num: this.state.selected_phoneme,
            input_text: this.state.input_text,
            font:this.state.font,
            blur:this.state.blur,
            image_width:this.state.image_width,
            image_height:this.state.image_height,
            is_invisiable:this.state.is_invisiable ? 1 : 0,
            color:[this.state.color],
            bg_filename:this.state.bg_filename,
            x_in_bg:this.state.x_in_bg,
            y_in_bg:this.state.y_in_bg
        })
            .then( response => {
                this.setState({
                    filename:response.data.filename,
                    cb_filename:response.data.cb_filename,
                    latter_list:response.data.latter_list,
                })
                this.get_sample(this.state.selected_latter, this.state.selected_phoneme, this.state.selected_phoneme2);
            })
            .catch( response => {
                this.setState({
                    is_loading:false                    
                })
                console.log(response);
            });    
    }

    update_phoneme_location(){
        if(!this.state.real_time)
            return;
        this.setState({
            is_loading:true
        })
        axios.put(domain+'/location', {
            latter_list:[this.state.latter_list],
            input_text: this.state.input_text,
            blur:this.state.blur,
            image_width:this.state.image_width,
            image_height:this.state.image_height,
            is_invisiable:this.state.is_invisiable ? 1 : 0,
            color:[this.state.color],
            bg_filename:this.state.bg_filename,
            x_in_bg:this.state.x_in_bg,
            y_in_bg:this.state.y_in_bg
        })
            .then( response => {
                this.setState({
                    filename:response.data.filename,
                    latter_list:response.data.latter_list,
                    is_loading:false
                })
            })
            .catch( response => {
                this.setState({
                    is_loading:false                    
                })
                console.log(response);
            });

    }

    update_phoneme_size(){
        if(!this.state.real_time)
            return;
        this.setState({
            is_loading:true
        })
        axios.put(domain+'/size', {
            latter_list:[this.state.latter_list],
            latter_num: this.state.selected_latter,
            phoneme_num: this.state.selected_phoneme,
            input_text: this.state.input_text,
            blur:this.state.blur,
            image_width:this.state.image_width,
            image_height:this.state.image_height,
            is_invisiable:this.state.is_invisiable ? 1 : 0,
            color:[this.state.color],
            bg_filename:this.state.bg_filename,
            x_in_bg:this.state.x_in_bg,
            y_in_bg:this.state.y_in_bg
        })
            .then( response => {
                this.setState({
                    filename:response.data.filename,
                    latter_list:response.data.latter_list,
                    is_loading:false
                })
            })
            .catch( response => {
                this.setState({
                    is_loading:false                    
                })
                console.log(response);
            });
    }

    update_phoneme_rotation(){
        if(!this.state.real_time)
            return;
        this.setState({
            is_loading:true
        })
        axios.put(domain+'/rotation', {
            latter_list:[this.state.latter_list],
            font:this.state.font,
            latter_num: this.state.selected_latter,
            phoneme_num: this.state.selected_phoneme,
            input_text: this.state.input_text,
            blur:this.state.blur,
            image_width:this.state.image_width,
            image_height:this.state.image_height,
            is_invisiable:this.state.is_invisiable ? 1 : 0,
            color:[this.state.color],
            bg_filename:this.state.bg_filename,
            x_in_bg:this.state.x_in_bg,
            y_in_bg:this.state.y_in_bg
        })
            .then( response => {
                this.setState({
                    filename:response.data.filename,
                    latter_list:response.data.latter_list,
                    is_loading:false
                })
            })
            .catch( response => {
                this.setState({
                    is_loading:false                    
                })
                console.log(response);
            });
    }
    set_color(e){
        let target = this.state.color;
        if(e.target.name == "red"){
            target[0] = e.target.value*=1;
            this.setState({color: target})
        }
        else if(e.target.name == "green"){
            target[1] = e.target.value*=1;
            this.setState({color: target})
        }else{
            target[2] = e.target.value*=1;
            this.setState({color: target})
        }
    }

    update_background_image(file){
        this.setState({
            is_loading:true
        })
        const formData = new FormData();
        formData.append('file', file);
        formData.append('filename', this.state.filename);
        formData.append('input_text', this.state.input_text);

        axios.post(domain+'/background', formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
        })
            .then( response => {
                this.setState({
                    bg_filename:response.data.bg_filename,
                    cb_filename:response.data.cb_filename,
                    is_loading:false
                })
            })
            .catch( response => {
                this.setState({
                    is_loading:false                    
                })
                console.log(response);
            });
    }

    generatePreviewImgUrl(file, callback) {
        const reader = new FileReader()
        const url = reader.readAsDataURL(file)
        reader.onloadend = e => callback(reader.result)
    }

    handleImage(e){
        const file = e.target.files[0]
        if (!file) return

        this.generatePreviewImgUrl(file, previewImgUrl => {
          this.setState({ previewImgUrl })
        })
        this.setState({
            selected_file : file,
        })
        this.update_background_image(file);
    }

    render(){
        const div_style={
            float:"left",
            marginLeft:"20px"
        }

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
                font={this.state.font}
                sliderChange={this.sliderChange}/>
        }else if(this.state.page == 1){
            html = 
            <div>
                <ImageOption
                    blur={this.state.blur}
                    image_width={this.state.image_width}
                    image_height={this.state.image_height}
                    handleChange={this.handleChange}
                    update_image_option={this.update_image_option}
                    color={this.state.color}
                    set_color={this.set_color}
                    handleImage={this.handleImage}
                    update_background_image={this.update_background_image}
                    is_invisiable={this.state.is_invisiable}
                    checkboxChange={this.checkboxChange}
                    cb_filename={this.state.cb_filename}
                    x_in_bg={this.state.x_in_bg}
                    y_in_bg={this.state.y_in_bg}
                />
                <div class="background-style">

                <ShowImage 
                    filename={this.state.filename}
                    cb_filename={this.state.cb_filename}
                    />
                <PhonemeList 
                    update_image={this.update_image}
                    latter_list={this.state.latter_list}
                    input_text={this.state.input_text}
                    select_phoneme={this.select_phoneme}
                />
                {this.state.selected_phoneme != -1 && 
                <PhonemeOption 
                    font={this.state.font}
                    phoneme2={this.state.selected_phoneme2}
                    phoneme={this.state.selected_phoneme}
                    latter={this.state.selected_latter}
                    latter_list={this.state.latter_list}
                    update_phoneme={this.update_phoneme}
                    update_phoneme_shape={this.update_phoneme_shape}
                    update_phoneme_size={this.update_phoneme_size}
                    update_phoneme_location={this.update_phoneme_location}
                    update_phoneme_rotation={this.update_phoneme_rotation}
                    toggle_real_time={this.toggle_real_time}
                    input_text={this.state.input_text}
                    handleChange={this.handleChange}
                    change_value={this.change_value}
                    style={div_style}
                    real_time={this.state.real_time}
                    sample={this.state.sample}
                    />

                }
                </div>
            </div>
                        
            
        }
        const loading = (
            <div class="loading-div">
                <div class="spinner">
                    <Spinner animation="border" variant="info" />
                </div>
            </div>
        )
        return(
            <div>
                {html}
                {this.state.is_loading && loading}
            </div>
        )
    }
}
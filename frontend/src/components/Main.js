import React from 'react';
import PhonemeList from './PhonemeList';
import axios from 'axios';
import ShowImage from './ShowImage';
import PhonemeOption from './PhonemeOption';
import ImageOption from './ImageOption';
import update from 'react-addons-update';
import InputText from './InputText';
import AddBackground from './AddBackground';
import {Spinner} from 'react-bootstrap'
import '../css/Main.css';
import '../css/normalize.css';
import '../css/demo.css';
import '../css/component.css';
import '../css/cs-select.css';
import '../css/cs-skin-boxes.css';

const domain ="http://13.124.118.44:5000/calligraphy";


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
            color:'000000',
            is_invisiable:false,
            selected_file:null,
            bg_filename:'',
            cb_filename:'',
            is_loading:false,
            x_in_bg:0,
            y_in_bg:0,
            real_time:true,
            sample:[],
            page2:0,
            page3:0,
            page4:0,
        };
        this.create_image = this.create_image.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleKeyPress = this.handleKeyPress.bind(this);
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
        this.set_location_in_bg = this.set_location_in_bg.bind(this);
        this.remove_background = this.remove_background.bind(this);
        this.nextPage = this.nextPage.bind(this);
        this.toVector = this.toVector.bind(this);
    }

    is_hangul_char(ch) {
        let c = ch.charCodeAt(0);
        if( 0x1100<=c && c<=0x11FF ) return true;
        if( 0x3130<=c && c<=0x318F ) return true;
        if( 0xAC00<=c && c<=0xD7A3 ) return true;
        return false;
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
                this.addPage(1);
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
        if(e.target.name.slice(0,1) === 'p'){
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
    handleKeyPress(e){
        if(e.key == 'Enter'){
            this.nextPage();
          }
    }
    checkboxChange(){
        let target = !this.state.is_invisiable;
        this.setState({
            is_invisiable:target
        })
        this.update_image_option(this.state.color, target);
    }

    update_image_option(color = this.state.color, is_invisiable = this.state.is_invisiable){
        this.setState({
            is_loading:true
        })
        axios.put(domain+'/image', {
            latter_list:[this.state.latter_list],
            blur:this.state.blur,
            image_width:this.state.image_width,
            image_height:this.state.image_height,
            color:color,
            is_invisiable:is_invisiable,
            input_text:this.state.input_text,
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
                console.log(response);
            })
            .catch( response => {
                this.setState({
                    is_loading:false                    
                })
                console.log(response);
            });
    }
    set_color(color){
        this.setState({
            color:color
        })
        this.update_image_option(color=color, this.state.is_invisiable);
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
            is_invisiable:this.state.is_invisiable,
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

    set_location_in_bg(){
        this.setState({is_loading:true})
        axios.put(domain+'/background/location', {
            input_text: this.state.input_text,
            filename:this.state.filename,
            bg_filename:this.state.bg_filename,
            x_in_bg:this.state.x_in_bg,
            y_in_bg:this.state.y_in_bg
        })
            .then( response => {
                this.setState({
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
    remove_background(){
        this.setState({
            bg_filename:'',
            cb_filename:''
        })
    }

    generatePreviewImgUrl(file, callback) {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onloadend = e => callback(reader.result)
    }

    handleImage(e){
        if(!this.state.is_invisiable){
            alert("투명성을 체크해야 해당 속성을 이용할 수 있습니다.");
            return;
        }
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

    addPage(page){
        page++;
        this.setState({
            page2:page
        })
        setTimeout(() => {
            this.setState({
                page3:page
            })
        }, 500);
        setTimeout(() => {
            this.setState({
                page4:page
            })
        }, 510);
    }

    nextPage(){
        let page = this.state.page2;
        if(page==0){
            if(this.state.input_text.length == 0){
                alert("한글을 입력해주세요!");
                return;
            }
            for(let c of this.state.input_text){
                if(!this.is_hangul_char(c)) {
                    alert("한글을 입력해주세요!");
                    return;
                }
            }
            this.addPage(page);
        }
        else if(page==1){
            this.create_image();
        }else{
            this.addPage(page);
        }
    }

    movePage(num){
        if(num<=1){
            const check = window.confirm("돌아가면 기존 작품은 삭제됩니다. 괜찮으세요?");
            if(!check) {
                this.setState({
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
                    color:'000000',
                    is_invisiable:false,
                    selected_file:null,
                    bg_filename:'',
                    cb_filename:'',
                    is_loading:false,
                    x_in_bg:0,
                    y_in_bg:0,
                    real_time:true,
                })
                return;
            }
        }
        if(num>=2 && this.state.filename == ''){
            alert("이전 과정을 완료해주세요.");
            return;
        }
        this.setState({
            page2:num
        })
        setTimeout(() => {
            this.setState({
                page3:num
            })
        }, 500);
        setTimeout(() => {
            this.setState({
                page4:num
            })
        }, 510);
    }
    toVector(){
        this.setState({
            is_loading:true
        })
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
        
        const li_list = [
            (<li className={"fs-li " + (this.state.page2 != 0 ? "fs-li-up" : "")}>
            <label className="fs-field-label fs-anim-upper" htmlFor="q1" >한글을 입력해주세요.</label>
            <input className="fs-anim-lower fs-input" onChange={this.handleChange} 
                id="q1" name="input_text" type="text" placeholder="" onKeyPress={this.handleKeyPress}
                autoComplete="off" required/>
            </li>),
            (
            <li className={"fs-li-down " + (this.state.page4 == 1 ? "fs-li" : "") + (this.state.page2 > 1 ? "fs-li-up" : "")}>
                <label class="fs-field-label fs-anim-upper" for="q3">폰트를 선택해주세요.</label>
                <div class="fs-radio-group fs-radio-custom clearfix fs-anim-lower">
                    <span><input id="q3b" name="font" value="0" onClick={this.handleChange} type="radio"/><label for="q3b" class="radio-conversion">날림체</label></span>
                    <span><input id="q3c" name="font" value="1" onClick={this.handleChange} type="radio"/><label for="q3c" class="radio-social">투박체</label></span>
                    <span><input id="q3a" name="font" value="2" onClick={this.handleChange} type="radio"/><label for="q3a" class="radio-mobile">장군체</label></span>
                </div>
            </li>
            ),
            (
            <li className={"fs-li-down " + (this.state.page4 == 2 ? "fs-li" : "") + (this.state.page2 > 2 ? "fs-li-up" : "")}>
                <label class="fs-field-label fs-anim-upper" >각 자, 모음의 모양을 결정합니다.</label><br/>
                <div className="inline-block width-50 vertical-top">

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
                </div>
                <div className="inline-block width-50">
                {this.state.selected_phoneme !== -1 && 
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
                    />}
                    </div>
            </li>
            ),
            (
                <li className={"fs-li-down " + (this.state.page4 == 3 ? "fs-li" : "") + (this.state.page2 > 3 ? "fs-li-up" : "")} data-input-trigger >
                    <label class="fs-field-label fs-anim-upper" data-info="We'll make sure to use it all over">이미지의 전체적인 옵션을 결정합니다.</label>
                    <br/>
                    <div className="inline-block width-50 vertical-top">
                        <ShowImage 
                        filename={this.state.filename}
                        cb_filename={this.state.cb_filename}
                        />
                    </div>
                    <div className="inline-block width-50 vertical-top margin-top-10">
                        <ImageOption
                            blur={this.state.blur}
                            image_width={this.state.image_width}
                            image_height={this.state.image_height}
                            handleChange={this.handleChange}
                            update_image_option={this.update_image_option}
                            color={this.state.color}
                            set_color={this.set_color}
                            is_invisiable={this.state.is_invisiable}
                            checkboxChange={this.checkboxChange}
                        />

                    </div>
                </li>
            ),
            (
                <li className={"fs-li-down " + (this.state.page4 == 4 ? "fs-li" : "") + (this.state.page2 > 4 ? "fs-li-up" : "")}>
                    <label class="fs-field-label fs-anim-upper" data-info="We'll make sure to use it all over">원하는 배경을 삽입합니다.</label>
                    <br/>
                    <div className="inline-block width-50 vertical-top">
                        <ShowImage 
                        filename={this.state.filename}
                        cb_filename={this.state.cb_filename}
                        />
                    </div>
                    <div className="inline-block width-50 vertical-top">
                        <AddBackground
                            handleImage={this.handleImage}
                            handleChange={this.handleChange}
                            set_location_in_bg={this.set_location_in_bg}
                            remove_background={this.remove_background}
                            x_in_bg={this.state.x_in_bg}
                            y_in_bg={this.state.y_in_bg}
                            cb_filename={this.state.cb_filename}/>

                    </div>
                </li>
            ),
            (
                <li className={"fs-li-down " + (this.state.page4 == 5 ? "fs-li" : "") + (this.state.page2 > 5 ? "fs-li-up" : "")}>
                    <div className="inline-block width-100 vertical-top">
                        <ShowImage 
                        filename={this.state.filename}
                        cb_filename={this.state.cb_filename}
                        />
                    </div>
                    <div class="text-center">
                        <button className="white bmp-to-vector" onClick={this.toVector}>Bitmap to Vector</button><br/>
                        <label class="fs-field-label fs-anim-upper" data-info="We'll make sure to use it all over">이미지를 부드럽게 만들어 줍니다.</label>
                    </div>
                    
                </li>
            )
        ]
        const btn_list = [];
        for(let i=0;i<6;i++){
            let btn = <button class = {this.state.page2 == i ? "fs-dot-current" : ""}
                        onClick={this.movePage.bind(this, i)}>                
            </button>
            btn_list.push(btn)
        }
        let fs_li = <div>
                        {li_list[this.state.page3]}
                    </div>
        let fs_div = <div className="fs-div">
                        <div className="fs-fields">{fs_li}</div>
                    </div>
        const fs_title = <div className="fs-title">
                            <h1>서로</h1>
                            <div className="codrops-top">
                                <a className="codrops-icon codrops-icon-prev" href="http://tympanus.net/Development/NotificationStyles/"><span>Previous Demo</span></a>
                                <a className="codrops-icon codrops-icon-drop" href="http://tympanus.net/codrops/?p=19520"><span>Back to the Codrops Article</span></a>
                                <a className="codrops-icon codrops-icon-info" href="#"><span>This is a demo for a fullscreen form</span></a>
                            </div>
                        </div>
        let fs_control = <div class="fs-controls">
                            <button class="fs-continue fs-show" onClick={this.nextPage}>Continue</button>
                            <nav class="fs-nav-dots fs-show">
                                {btn_list}
                            </nav>
                            <span class="fs-numbers fs-show">
                                <span class="fs-number-current">{this.state.page2 + 1}</span>
                                <span class="fs-number-total">6</span>
                            </span>
                            <div class="fs-progress fs-show"></div>
                        </div>
        let form_wrap = <div className="fs-form-wrap" id="fs-form-wrap">
                            {fs_title}
                            {fs_div}
                            {fs_control}
                        </div>

        let related = <div className="related">
                        <p>If you enjoyed this demo you might also like:</p>
                        <a href="http://tympanus.net/Development/MinimalForm/">
                            <img src="img/relatedposts/minimalform1-300x162.png" />
                            <h3>Minimal Form Interface</h3>
                        </a>
                        <a href="http://tympanus.net/Development/ButtonComponentMorph/">
                            <img src="img/relatedposts/MorphingButtons-300x162.png" />
                            <h3>Morphing Buttons Concept</h3>
                        </a>
                    </div>
        let container = <div className="container">
                            {form_wrap}
                            {related}
                        </div>
        const loading = (
            <div className="loading-div">
                <div className="spinner">
                    <Spinner animation="border" variant="info" />
                </div>
            </div>
        )

        return(
        <div class="container">
                {container}
                {this.state.is_loading && loading}
        </div>
        )
    }
}
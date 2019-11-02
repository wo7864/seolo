import React from 'react';
import img from '../static/image/test.png'
import '../css/ShowImage.css';
export default class ShowImage extends React.Component {
    constructor(props){
        super(props);
    }

    render(){

        let filename = this.props.filename;
        if(this.props.cd_filename){
            filename = this.props.cd_filename;
        }
        const img_dir = 'http://seolo.s3-website.ap-northeast-2.amazonaws.com/static/image/'+filename;
        const image = (
            <a href={img_dir} >
                <img src={img} class="image_style"/>
            </a>
        )
        return(
            <div class="text-center my-auto">
                {image}
            </div>
        )
    }
}


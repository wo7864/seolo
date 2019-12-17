import React from 'react';
import '../css/ShowImage.css';
export default class ShowImage extends React.Component {
    render(){

        let filename = this.props.filename;
        if(this.props.cb_filename){
            filename = this.props.cb_filename;
        }
        //const img_dir = 'http://seolo.s3-website.ap-northeast-2.amazonaws.com/static/image/'+filename;
        const img_dir = '/images/result/'+filename;

        const image = (
                <img src={img_dir} className="image_style" alt=""/>
        )
        return(
            <div className="text-center my-auto image-div">
                {image}
            </div>
        )
    }
}


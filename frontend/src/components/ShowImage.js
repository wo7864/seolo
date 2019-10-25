import React from 'react';


export default class ShowImage extends React.Component {
    constructor(props){
        super(props);
    }
    render(){
        let filename = this.props.filename

        const img_dir = 'http://seolo.s3-website.ap-northeast-2.amazonaws.com/static/image/'+filename;
        const image = (
            <a href={img_dir}>
                <img src={img_dir}/>
            </a>
        )
        return(
            <div>
                {image}
            </div>
        )
    }
}


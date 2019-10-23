import React from 'react';


export default class ShowImage extends React.Component {
    constructor(props){
        super(props);
    }
    render(){
        let filename = this.props.filename

        const img_dir = 'file:///C:/Users/wo786/api/static/image/'+filename;
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


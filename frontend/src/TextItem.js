import React from "react";

const TextItem = ({ text, id, handleClick }) => {
  return (
    <div>
      <p>{text}</p>
      <button onClick={() => handleClick(id)}>삭제</button>
    </div>
  );
};

export default TextItem;


import React from 'react';
import { useDispatch } from 'react-redux';
import { setCurrentChunkIndex } from './store/articlesSlice';


// Define an interface for the props
interface MyComponentProps {
    chunk: {
        text: string,
        index: number
    };
    active: boolean;
  }
  
// Functional component with typed props
const Chunk: React.FC<MyComponentProps> = ({ chunk, active }) => {

    const dispatch = useDispatch();

    const handleOnClick = () => { 
        dispatch(setCurrentChunkIndex(chunk.index));
    }

    return (
        <div className={ active ? "mb-4 text-yellow-200" : "mb-4"} onClick={handleOnClick}>
            <p>{chunk.text}</p>
        </div>
    )
}

export default Chunk
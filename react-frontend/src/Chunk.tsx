
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setArticles, setSelectedArticle, setCurrentChunkIndex } from './store/articlesSlice';
import axiosInstance from './axiosInstance'; // Import the configured axios instance
import { RootState } from './store';

// Define an interface for the props
interface MyComponentProps {
    text: string;
    active: boolean;
  }
  
// Functional component with typed props
const Chunk: React.FC<MyComponentProps> = ({ text, active }) => {

    return (
        <div className={ active ? "mb-4 text-yellow-200" : "mb-4"}>
            <p>{text}</p>
        </div>
    )
}

export default Chunk
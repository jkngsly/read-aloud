// src/App.tsx

import React, { useEffect, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setArticles, setSelectedArticle, setCurrentChunkIndex } from './store/articlesSlice';
import axiosInstance from './axiosInstance'; // Import the configured axios instance
// @ts-ignore
import { RootState } from './store';
import Chunk from './Chunk.tsx';

const App = () => {
  const dispatch = useDispatch();
  const { articles, selectedArticle, currentChunkIndex } = useSelector(
    (state: RootState) => state.articles
  );

  const audioRef = useRef<HTMLAudioElement>(null)

  useEffect(() => {
    // Fetch articles list using axiosInstance
    const fetchArticles = async () => {
      try {
        const response = await axiosInstance.get('/get-articles');
        dispatch(setArticles(response.data.articles));
      } catch (error) {
        console.error('Error fetching articles:', error);
      }
    };

    fetchArticles();
  }, [dispatch]);

  useEffect(() => {
    // When the current chunk changes, update the audio source and play it
    if (selectedArticle && currentChunkIndex >= 0) {
      const currentChunk = selectedArticle.chunks[currentChunkIndex];

      // Make API request to get the MP3 URL
      const fetchAudio = async () => {
        try {
          const response = await axiosInstance.get(`/get-audio?path=${encodeURIComponent(currentChunk.audio_path)}`, {
            responseType: 'blob', 
          });

          // Convert the blob into an object URL
          const objectUrl = URL.createObjectURL(response.data);
        
          if (audioRef.current) {
      
            // Assuming the response contains a valid URL
            audioRef.current.src = objectUrl;
            audioRef.current.play();
          }
        } catch (error) {
          console.error('Error fetching audio file:', error);
        }
      };

      fetchAudio();
    }
  }, [currentChunkIndex, selectedArticle]);

  const handleArticleClick = async (path: string) => {
    // Fetch article metadata using axiosInstance
    try {
      const response = await axiosInstance.get(`/get-article-metadata?path=${encodeURIComponent(path)}`);
      dispatch(setSelectedArticle(response.data));
    } catch (error) {
      console.error('Error fetching article metadata:', error);
    }
  };

  const handlePrevChunk = () => {
    if (selectedArticle && currentChunkIndex > 0) {
      dispatch(setCurrentChunkIndex(currentChunkIndex - 1));
    }
  };

  const handleNextChunk = () => {
    if (selectedArticle && currentChunkIndex < selectedArticle.chunks.length - 1) {
      dispatch(setCurrentChunkIndex(currentChunkIndex + 1));
    }
  };

  const currentChunk = selectedArticle?.chunks[currentChunkIndex];

  return (
    <>
      <div className="flex w-full h-20 bg-gray-600">
        <h2>Read Aloud</h2>
      </div>
      <div className="flex w-full">
        <div className="w-full flex">
          {/* Left Side: List of Articles */}
          <div className="w-1/3 mr-6">
            <h2 className="text-2xl font-semibold mb-4">Articles</h2>
            <ul className="space-y-4">
              {articles.map((article: any) => (
                <li
                  key={article.path}
                  className="cursor-pointer hover:text-blue-500"
                  onClick={() => handleArticleClick(article.path)}
                >
                  {article.title}
                </li>
              ))}
            </ul>
          </div>

          {/* Right Side: Selected Article and Audio Player */}
          <div className="w-2/3">
            {selectedArticle ? (
              <>
                <h2 className="text-xl font-semibold mb-4">{selectedArticle.title}</h2>

                <div className="overflow-y-scroll h-96"> 
                    {selectedArticle.chunks.map((chunk: any, index: number) => {
                    return <Chunk chunk={{...chunk, index: index}} active={currentChunkIndex === index} key={index} />;
                    })}
                </div>
                
                {/* Audio Player */}
                <div className="flex items-center">
                  <button
                    onClick={handlePrevChunk}
                    className="px-4 py-2 bg-blue-500 text-white rounded mr-2"
                  >
                    Prev
                  </button>

                  <audio ref={audioRef} controls onEnded={handleNextChunk}>
                    <source
                      src={`/${currentChunk?.audio_path}`}
                      type="audio/mpeg"
                    />
                    Your browser does not support the audio element.
                  </audio>

                  <button
                    onClick={handleNextChunk}
                    className="px-4 py-2 bg-blue-500 text-white rounded ml-2"
                  >
                    Next
                  </button>
                </div>
              </>
            ) : (
              <p>Select an article to view</p>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default App;

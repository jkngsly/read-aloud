// src/App.tsx

import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setArticles, setSelectedArticle, setCurrentChunkIndex } from './store/articlesSlice';
import axiosInstance from './axiosInstance'; // Import the configured axios instance
import { RootState } from './store';

const App = () => {
  const dispatch = useDispatch();
  const { articles, selectedArticle, currentChunkIndex } = useSelector(
    (state: RootState) => state.articles
  );

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
    <div className="flex p-6">
      {/* Left Side: List of Articles */}
      <div className="w-1/3 mr-6">
        <h2 className="text-2xl font-semibold mb-4">Articles</h2>
        <ul className="space-y-4">
          {articles.map((article) => (
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
            <div className="mb-4">
              <p>{currentChunk?.text}</p>
            </div>

            {/* Audio Player */}
            <div className="flex items-center">
              <button
                onClick={handlePrevChunk}
                className="px-4 py-2 bg-blue-500 text-white rounded mr-2"
              >
                Prev
              </button>

              <audio controls>
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
  );
};

export default App;

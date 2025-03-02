// src/store/articlesSlice.ts

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Chunk {
  text: string;
  audio_path: string;
}

interface Article {
  title: string;
  path: string;
  chunks: Chunk[];
}

interface ArticlesState {
  articles: Article[];
  selectedArticle: Article | null;
  currentChunkIndex: number;
}

const initialState: ArticlesState = {
  articles: [],
  selectedArticle: null,
  currentChunkIndex: 0,
};

const articlesSlice = createSlice({
  name: 'articles',
  initialState,
  reducers: {
    setArticles: (state, action: PayloadAction<Article[]>) => {
      state.articles = action.payload;
    },
    setSelectedArticle: (state, action: PayloadAction<Article>) => {
      state.selectedArticle = action.payload;
      state.currentChunkIndex = 0; // Reset chunk index when new article is selected
    },
    setCurrentChunkIndex: (state, action: PayloadAction<number>) => {
      state.currentChunkIndex = action.payload;
    },
  },
});

export const { setArticles, setSelectedArticle, setCurrentChunkIndex } = articlesSlice.actions;

export default articlesSlice.reducer;
